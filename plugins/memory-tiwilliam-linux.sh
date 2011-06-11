#!/bin/bash

if [ ! -d /proc ]; then
	echo "Error: No proc filesystem not found"
	exit 1
fi

if [ "$1" == "config" ]; then
	echo "interval 10"
	exit
fi

for label in MemTotal MemFree Buffers Cached Active Inactive SwapCached SwapTotal; do
	temp=$(cat /proc/meminfo | egrep "^$label:" | awk '{ print $2 }')
	echo "$label.value $temp"
done
