#!/bin/bash

if [ "$1" == "config" ]; then
	echo "interval 10"
	exit
fi

mounts=$(cat /proc/mounts | egrep "^tmpfs" | cut -d ' ' -f 2)

for mount in $mounts; do
	total=$(df $mount | tail -1 | awk '{ print $2 }')
	used=$(df $mount | tail -1 | awk '{ print $3 }')
	free=$(df $mount | tail -1 | awk '{ print $4 }')
	echo "${mount}_total.value $total"
	echo "${mount}_used.value $used"
	echo "${mount}_free.value $free"
done
