#!/bin/sh

if [ "$1" == "config" ]; then
	echo "interval 10"
	exit
fi

threads=$(ps -AT | egrep -vc "PID|TTY")
maxthreads=$(cat /proc/sys/kernel/threads-max)

echo "maxtreads.value $maxthreads"
echo "treads.value $threads"
