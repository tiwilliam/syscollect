#!/bin/bash

load1=$(cat /proc/loadavg | cut -d ' ' -f 1)
load2=$(cat /proc/loadavg | cut -d ' ' -f 2)
load3=$(cat /proc/loadavg | cut -d ' ' -f 3)

echo "load1 $load1"
echo "load2 $load2"
echo "load3 $load3"
