#!/bin/bash

# LCK.lol_2.0/update.sh

filename=update_$(date +%y%m%d_%H:%M:%S).log
{
	date +%y/%m/%d_%H:%M:%S
	python3 /home/ubuntu/LCK.lol_2.0/manage.py update
} > "/home/ubuntu/LCK.lol_2.0/log/$filename" 2>&1
