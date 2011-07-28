#!/bin/bash

if [ ! -d /proc ]; then
	echo "Error: No proc fs found"
	exit 1
fi

uptime=$(cat /proc/uptime | cut -d ' ' -f 1)

echo "uptime $uptime"
