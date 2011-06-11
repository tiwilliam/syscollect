#!/bin/sh

if [ "$1" == "config" ]; then
#	echo "interval 10"
	exit
fi

load1=$(cat /proc/loadavg | cut -d ' ' -f 1)
load2=$(cat /proc/loadavg | cut -d ' ' -f 2)
load3=$(cat /proc/loadavg | cut -d ' ' -f 3)

echo "load1.value $load1"
echo "load2.value $load2"
echo "load3.value $load3"
