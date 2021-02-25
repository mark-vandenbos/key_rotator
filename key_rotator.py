import argparse
import boto3
from botocore.exceptions import ClientError
import json, time, datetime, sys


iam_client = boto3.client('iam')
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="An IAM username, e.g. key_rotator.py --username <username>")
parser.add_argument("-k", "--key", help="An AWS access key, e.g. key_rotator.py --key <access_key>")
parser.add_argument("--rotate", help="create, disable, delete", action="store_true")
args = parser.parse_args()
username = args.username
aws_access_key = args.key



def create_key(username):
    access_key_metadata = iam_client.create_access_key(UserName=username)['AccessKey']
    access_key = access_key_metadata['AccessKeyId']
    secret_key = access_key_metadata['SecretAccessKey']
    print(f"access key created\naws_access_key_id = {access_key}\naws_secret_access_key = {secret_key}\n")
    access_key = ''
    secret_key = ''


def disable_key(access_key, username):
    try:
        iam_client.update_access_key(UserName=username, AccessKeyId=access_key, Status="Inactive")
        print(f"access key {access_key} disabled\n")
    except ClientError as e:
        print(f"access key {access_key} not found\n")


def delete_key(access_key, username):
    try:
        iam_client.delete_access_key(UserName=username, AccessKeyId=access_key)
        print(f"access key {access_key} deleted\n")
    except ClientError as e:
        print(f"access key {access_key} not found\n")


def list_keys(keys):
    key_count = 0
    print(f"key list for username: {username}") 
    for key in keys['AccessKeyMetadata']:

        keydate = key['CreateDate']
        keydate = keydate.strftime("%Y-%m-%d %H:%M:%S")
        currentdate = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        accesskeyd = time.mktime(datetime.datetime.strptime(keydate, "%Y-%m-%d %H:%M:%S").timetuple())
        currentd = time.mktime(datetime.datetime.strptime(currentdate, "%Y-%m-%d %H:%M:%S").timetuple())
        active_days = (currentd - accesskeyd)/60/60/24

        key_count = key_count + 1
        print(f"access key: {key['AccessKeyId']} (age: {active_days:.0f}d, status: {key['Status']})")

    print("\n")
    return key_count


try:
    key_count = list_keys(iam_client.list_access_keys(UserName=username))
    if key_count >= 2:
        print(f"username {username} has 2 keys, you must delete a key before continuing")

    if args.rotate: 
        create_key(username)
        disable_key(aws_access_key, username)
        delete_key(aws_access_key, username)
        key_count = list_keys(iam_client.list_access_keys(UserName=username))


except ClientError as e:
    print("username {username} not found.")





