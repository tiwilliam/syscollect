#!/bin/ksh

if [ "$1" == "config" ]; then
	echo "interval 2"
	exit 0
fi

cpus=$(/sbin/sysctl hw.ncpufound | cut -d '=' -f 2)
cores=$(/sbin/sysctl hw.ncpu | cut -d '=' -f 2)
cpu_user=$(/sbin/sysctl kern.cp_time | cut -d '=' -f 2 | cut -d ',' -f 1)
cpu_nice=$(/sbin/sysctl kern.cp_time | cut -d '=' -f 2 | cut -d ',' -f 2)
cpu_sys=$(/sbin/sysctl kern.cp_time | cut -d '=' -f 2 | cut -d ',' -f 3)
cpu_irq=$(/sbin/sysctl kern.cp_time | cut -d '=' -f 2 | cut -d ',' -f 4)
cpu_idle=$(/sbin/sysctl kern.cp_time | cut -d '=' -f 2 | cut -d ',' -f 5)

for value in cores cpu_user cpu_nice cpu_sys cpu_irq cpu_idle; do
	eval data=\$${value}
	echo "$value.value $data"
done
