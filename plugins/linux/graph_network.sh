#!/bin/bash

if [ ! -d /proc ]; then
	echo "Error: No proc fs found"
	exit 1
fi

if [ ! -f /proc/net/dev ]; then
	echo "Error: /proc/net/dev not found"
	exit 1
fi

devs=$(cat /proc/net/dev | egrep "^[ ]*[0-9A-Za-z]+:" | cut -d ':' -f 1 | tr -d ' ')

for dev in $devs; do
	recv=$(cat /proc/net/dev | egrep "^[ ]*$dev:" | cut -d ':' -f 2 | awk '{ print $1 }')
	sent=$(cat /proc/net/dev | egrep "^[ ]*$dev:" | cut -d ':' -f 2 | awk '{ print $9 }')
	rerr=$(cat /proc/net/dev | egrep "^[ ]*$dev:" | cut -d ':' -f 2 | awk '{ print $2 }')
	serr=$(cat /proc/net/dev | egrep "^[ ]*$dev:" | cut -d ':' -f 2 | awk '{ print $10 }')
	rdrop=$(cat /proc/net/dev | egrep "^[ ]*$dev:" | cut -d ':' -f 2 | awk '{ print $3 }')
	sdrop=$(cat /proc/net/dev | egrep "^[ ]*$dev:" | cut -d ':' -f 2 | awk '{ print $11 }')

	echo "${dev}.recv $recv"
	echo "${dev}.sent $sent"
	echo "${dev}.rerr $rerr"
	echo "${dev}.serr $serr"
	echo "${dev}.rdrop $rdrop"
	echo "${dev}.sdrop $sdrop"
done
