# Cross-platform graph and system info distribution

Graphd have as goal to make server graphing easy and platform independent.

Currently supported platforms:

* Linux
* FreeBSD
* OpenBSD
* Darwin
* Windows

### How does it work?

	$ nc localhost 8090
	# darwin.defunct.cc graphd 0.5.0

	lsgraph
	["darwin/graph_cpu", "darwin/graph_loadavg"]

	fetch darwin/graph_cpu
	{"cpu_nice": [
		[1309200447, "15"],
		[1309200452, "15"],
		[1309200457, "16"],
		[1309200462, "16"],
		...
	]}

	lsinfo
	["darwin/info_os"]

	fetch darwin/info_os
	{"os_version": [
		[1309200467, "Mac OS X 10.7"]
	]}

### Write your own plugins

	$ ls -l /etc/graphd/plugins
	total 0
	drwxr-xr-x  5 wille  staff  170 Jun 25 16:58 darwin
	drwxr-xr-x  4 wille  staff  136 Jun 25 15:17 freebsd
	drwxr-xr-x  9 wille  staff  306 Jun 25 16:57 linux
	drwxr-xr-x  2 wille  staff   68 Jun 25 15:06 noarch
	drwxr-xr-x  4 wille  staff  136 Jun 25 15:09 openbsd
    
	$ ls -l /etc/graphd/plugins/darwin
	total 40
	-rw-r--r--  1 wille  staff  1392 Jun 25 13:57 graph_cpu.c
	-rw-r--r--  1 wille  staff   102 Jun 25 15:55 graph_cpu.conf
	-rwxr-xr-x  1 wille  staff  8992 Jun 25 15:55 graph_cpu
	-rwxr-xr-x  1 wille  staff   391 Jun 25 15:27 graph_loadavg
	-rw-r--r--  1 wille  staff   102 Jun 25 15:27 graph_loadavg.conf
	-rwxr-xr-x  1 wille  staff   405 Jun 25 16:23 info_os
	-rw-r--r--  1 wille  staff   125 Jun 25 16:23 info_os.conf

	$ cat /etc/graphd/plugins/darwin/graph_cpu.conf
	interval 10
