#!/bin/bash

load1=$(uptime | sed 's/.*load averages: \([0-9 \.]*\)$/\1/' | cut -d ' ' -f 1)
load2=$(uptime | sed 's/.*load averages: \([0-9 \.]*\)$/\1/' | cut -d ' ' -f 2)
load3=$(uptime | sed 's/.*load averages: \([0-9 \.]*\)$/\1/' | cut -d ' ' -f 3)

echo "load1.value $load1"
echo "load2.value $load2"
echo "load3.value $load3"
