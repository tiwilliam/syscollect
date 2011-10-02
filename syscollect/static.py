import os
import socket

try:
    system = os.uname()[0]
except:
    system = 'Windows'

ttl = 300
loglevel = 'debug'
name = 'syscollect'

types = [ 'graph', 'info' ]
ignoresuffix = [ 'disabled', 'c', 'conf' ]

major = 0
minor = 5
patch = 0
version = str(major) + '.' + str(minor) + '.' + str(patch)

fqdn = socket.gethostname()

if system == 'Windows':
	base_path = os.getenv('PROGRAMFILES', 'C:\\Program Files')
	plug_path = base_path + '\\' + name + '\\plugins'
else:
	plug_path = '/etc/' + name.lower() + '/plugins'
