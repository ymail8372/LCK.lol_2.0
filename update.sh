#!/bin/bash

# update script
# LCK.lol_2.0/update.sh

{
date
source "/home/ubuntu/myvenv/bin/activate"
python3 /srv/LCK.lol_2.0/manage.py update
} >> /srv/LCK.lol_2.0/log/update.log 2>&1
