# AWS Access key rotator

AWS Access key rotator. 

This script will display and or rotate current access keys(s) age and and status. 

Usage: 

    python key_rotator.py \
    --username <username> \
    --key <access_key>

Optional flags:

    --rotate    (rotate the provided keys (create new, disable provided key, delete provided key))


# Credit

Based on/adapted from [jicowan/key_rotator](https://github.com/jicowan/key_rotator/blob/master/key_rotator.py) 