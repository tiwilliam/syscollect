import os
import time
import signal

import tcp
import util
import repository

def gotsignal(signum, frame):
	if signum == signal.SIGINT:
		logger.info('Received interrupt signal - bye')
		os.sys.exit(0)
	if signum == signal.SIGHUP:
		logger.info('Reloading plugin directory')
		repo.reload_plugins()

ttl = 300
path = 'plugins'
loglevel = 'debug'

logger = util.logger(loglevel)
system = os.uname()[0]

signal.signal(signal.SIGINT, gotsignal)
signal.signal(signal.SIGHUP, gotsignal)

logger.info('You are running ' + system)

repo = repository.Repository(path, system.lower(), ttl)
loaded_plugins = repo.get_plugins()

if loaded_plugins:
	for p in loaded_plugins:
		p.start()
else:
	logger.error('No plugins found - bye')
	os.sys.exit(1)

def mgmt_list(args):
	plist = ''
	for p in loaded_plugins:
		plist += p.id + ' '
	return plist

def mgmt_fetch(args):
	if args:
		plugin_id = args[1]

	return '90348 90213849012849 0128490128 90421'

server = tcp.ThreadedServer(('', 8090), tcp.RequestHandler)

server.add_callback('list', mgmt_list)
server.add_callback('fetch', mgmt_fetch)

server.serve()
