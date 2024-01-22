#!/bin/bash

# LCK.lol_2.0/update.sh

filename=update_$(date +%y%m%d_%H:%M:%S).log
{
	date +%y/%m/%d_%H:%M:%S
	source /home/ubuntu/myvenv/bin/activate
	python3 /srv/LCK.lol_2.0/manage.py update
} > "/srv/LCK.lol_2.0/log/$filename" 2>&1
