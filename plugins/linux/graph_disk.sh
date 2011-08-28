#!/bin/bash

if [ ! -d /proc ]; then
	echo "Error: No proc fs found"
	exit 1
fi

mounts=$(cat /proc/mounts | egrep -v "^none|rootfs|tmpfs|udev|devpts|usbfs|fusectl" | cut -d ' ' -f 2)

for mount in $mounts; do
	total=$(df -P $mount | tail -1 | awk '{ print $2 }')
	used=$(df -P $mount | tail -1 | awk '{ print $3 }')
	free=$(df -P $mount | tail -1 | awk '{ print $4 }')
	echo "${mount}.total $total"
	echo "${mount}.used $used"
	echo "${mount}.free $free"
done