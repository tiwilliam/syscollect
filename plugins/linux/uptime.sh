#!/bin/bash

if [ ! -d /proc ]; then
	echo "Error: No proc filesystem not found"
	exit 1
fi

if [ "$1" == "config" ]; then
	echo "interval 60"
	exit
fi

uptime=$(cat /proc/uptime | cut -d ' ' -f 1)

echo "uptime.value $uptime"
