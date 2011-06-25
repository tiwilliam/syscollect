#!/bin/bash

if [ "$1" == "config" ]; then
	echo "interval 10"
	exit
fi

load1=$(uptime | sed 's/.*load averages: //' | cut -d ',' -f 1 | awk '{print $1}')
load2=$(uptime | sed 's/.*load averages: //' | cut -d ',' -f 2 | awk '{print $1}')
load3=$(uptime | sed 's/.*load averages: //' | cut -d ',' -f 3 | awk '{print $1}')

echo "load1.value $load1"
echo "load2.value $load2"
echo "load3.value $load3"