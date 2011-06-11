#!/bin/sh

if [ "$1" == "config" ]; then
	echo "interval 2"
	exit
fi

cpus=$(cat /proc/cpuinfo | grep "physical id" | sort | uniq | wc -l)
cores=$(cat /proc/cpuinfo | grep -c "core id")
cpu_user=$(cat /proc/stat | head -1 | awk '{ print $2 }')
cpu_nice=$(cat /proc/stat | head -1 | awk '{ print $3 }')
cpu_sys=$(cat /proc/stat | head -1 | awk '{ print $4 }')
cpu_idle=$(cat /proc/stat | head -1 | awk '{ print $5 }')
cpu_iowait=$(cat /proc/stat | head -1 | awk '{ print $6 }')
cpu_irq=$(cat /proc/stat | head -1 | awk '{ print $7 }')
cpu_softirq=$(cat /proc/stat | head -1 | awk '{ print $8 }')

for value in cpu_user cpu_nice cpu_sys cpu_idle cpu_iowait cpu_irq cpu_softirq; do
	echo "$value.value $[$value]"
done
