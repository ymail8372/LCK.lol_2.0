#!/bin/bash

filename=update_$(date +%y%m%d_%H:%M:%S).log
{
	date +%y/%m/%d_%H:%M:%S
	python3 $LCKINFO_HOME/manage.py update
} > "$LCKINFO_HOME/log/$filename" 2>&1
