# Cross-platform graph data server

Graphd have as goal to make server graphing easy and platform independent.

Currently supported platforms:

* Linux
* FreeBSD
* OpenBSD
* Darwin

### How does it work?

    $ nc localhost 8090
    # darwin.defunct.cc graphd 0.5.0

	list
	darwin/cpu.o darwin/loadavg.sh
	
    fetch darwin/cpu.o
    {"cpu_nice": [[1309200447, "15"], [1309200452, "15"], [1309200457, "16"], [1309200462, "16"]...}

    fetch darwin/cpu.o 1309200462
    {"cpu_nice": [[1309200467, "16"], [1309200472, "18"], [1309200477, "18"], [1309200482, "19"]...}

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
    -rw-r--r--@ 1 wille  staff  1392 Jun 25 13:57 cpu.c
    -rwxr-xr-x  1 wille  staff  8992 Jun 25 15:55 cpu.o
    -rwxr-xr-x@ 1 wille  staff   391 Jun 25 15:27 loadavg.sh