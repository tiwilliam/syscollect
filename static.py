import os
import socket

ttl = 300
path = '/etc/graphd/plugins'
loglevel = 'debug'

name = 'graphd'

major = 0
minor = 5
patch = 0
version = str(major) + '.' + str(minor) + '.' + str(patch)

fqdn = socket.gethostname()
system = os.uname()[0]
