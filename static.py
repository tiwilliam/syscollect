import os
import socket

try:
    system = os.uname()[0]
except:
    system = 'Windows'

ttl = 300
loglevel = 'debug'
name = 'graphd'
ignoresuffix = [ 'conf', 'c' ]

major = 0
minor = 5
patch = 0
version = str(major) + '.' + str(minor) + '.' + str(patch)

fqdn = socket.gethostname()

if system == 'Windows':
	path = os.getenv('PROGRAMFILES', 'C:\\Program Files') + '\\' + name + '\\plugins'
else:
	path = '/etc/' + name.lower() + '/plugins'
