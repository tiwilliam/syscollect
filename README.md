# Cross-platform system data collector
---
Time to make data collecting easy and platform independent!

Currently supported platforms:

* Linux
* FreeBSD
* OpenBSD
* Darwin
* Windows

### How does it work?

	$ nc localhost 8090
	# darwin.defunct.cc syscollect 0.5.0

	list
	["cpu", "loadavg", "os"]

	fetch cpu
	{"time": 1309200447,
	 "data": {
	 	"sys": [
			[0, "15"],
			[5, "15"],
			[10, "16"],
			...
		],
		"user": [
			[0, "2425"],
			[5, "2428"],
			[10, "2432"],
			...
		]
	 }
	}
	
	fetch os
	{"time": 1309200447,
	 "version": [
		[0, "Mac OS X 10.7"]
	 ]
	}

### Write your own plugins

	$ ls -l /etc/syscollect/plugins
	total 0
	drwxr-xr-x  5 wille  staff  170 Jun 25 16:58 darwin
	drwxr-xr-x  4 wille  staff  136 Jun 25 15:17 freebsd
	drwxr-xr-x  9 wille  staff  306 Jun 25 16:57 linux
	drwxr-xr-x  2 wille  staff   68 Jun 25 15:06 noarch
	drwxr-xr-x  4 wille  staff  136 Jun 25 15:09 openbsd
    
	$ ls -l /etc/syscollect/plugins/darwin
	total 40
	-rw-r--r--  1 wille  staff  1392 Jun 25 13:57 cpu.c
	-rwxr-xr-x  1 wille  staff  8992 Jun 25 15:55 cpu
	-rwxr-xr-x  1 wille  staff   391 Jun 25 15:27 loadavg
	-rwxr-xr-x  1 wille  staff   405 Jun 25 16:23 os
