#!/bin/bash

# update script
# LCK.lol_2.0/update.sh

{
date
/Library/Frameworks/Python.framework/Versions/3.10/bin/python3 /Users/kimminseok/Library/Mobile\ Documents/com~apple~CloudDocs/Desktop/coding/LCKlol/manage.py update
echo "-------------------------------------"
} >> /Users/kimminseok/Library/Mobile\ Documents/com~apple~CloudDocs/Desktop/coding/LCKlol/log/update.log 2>&1

