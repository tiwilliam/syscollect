#include <stdio.h>
#include <mach/host_info.h>

int get_cpu_ticks();

int main(int argc, char *argv[])
{
	int ret = get_cpu_ticks();
	
	return ret;
}

int get_cpu_ticks()
{
	int err;
	mach_msg_type_number_t count;
	natural_t user, sys, idle, nice, cpus, cores;
	
	host_basic_info_data_t basic_info;
	host_cpu_load_info_data_t cpu_load;
	
	mach_port_t host_port = mach_host_self();
	
	count = HOST_BASIC_INFO_COUNT;
	err = host_info(host_port, HOST_BASIC_INFO, (host_info_t) &basic_info, &count);
	
	if (err)
	{
		printf("Failed to get host basic info\n");
		return 1;
	}
	
	count = HOST_CPU_LOAD_INFO_COUNT;
	err = host_statistics(host_port, HOST_CPU_LOAD_INFO, (host_info_t) &cpu_load, &count);
	
	if (err)
	{
		printf("Failed to get cpu load info\n");
		return 1;
	}
	
	/*
	if (basic_info.logical_cpu > 0)
		cpus = basic_info.avail_cpus / basic_info.logical_cpu;
	*/
	
	cores = basic_info.avail_cpus;
	user = cpu_load.cpu_ticks[CPU_STATE_USER];
	sys = cpu_load.cpu_ticks[CPU_STATE_SYSTEM];
	idle = cpu_load.cpu_ticks[CPU_STATE_IDLE];
	nice = cpu_load.cpu_ticks[CPU_STATE_NICE];
	
	printf("cores.value %d\n", cores);
	printf("cpu_user.value %d\n", user);
	printf("cpu_nice.value %d\n", nice);
	printf("cpu_sys.value %d\n", sys);
	printf("cpu_idle.value %d\n", idle);
	
	return 0;
}
