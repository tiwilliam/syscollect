#!/bin/bash

if [ "$1" == "config" ]; then
	echo "interval 10"
	exit
fi

for label in MemTotal MemFree Buffers Cached Active Inactive SwapCached SwapTotal; do
	temp=$(cat /proc/meminfo | egrep "^$label:" | awk '{ print $2 }')
	echo "$label.value $temp"
done
