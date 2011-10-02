#!/bin/bash

if [ ! -d /proc ]; then
	echo "Error: No proc fs found"
	exit 1
fi

for label in MemTotal MemFree Buffers Cached Active Inactive SwapCached SwapTotal; do
	temp=$(cat /proc/meminfo | egrep "^$label:" | awk '{ print $2 }')
	echo "$label $temp"
done
