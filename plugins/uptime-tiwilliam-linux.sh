#!/bin/sh

if [ "$1" == "config" ]; then
	echo "interval 10"
	exit
fi

uptime=$(cat /proc/uptime | cut -d ' ' -f 1)

echo "uptime.value $uptime"
