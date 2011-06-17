import os
import time
import signal

import tcp
import util
import static
import repository

def gotsignal(signum, frame):
	if signum == signal.SIGINT:
		logger.info('Received interrupt signal - bye')
		os.sys.exit(0)
	if signum == signal.SIGHUP:
		logger.info('Reloading plugin directory')
		repo.reload_plugins()

logger = util.logger(static.loglevel)
system = os.uname()[0]

signal.signal(signal.SIGINT, gotsignal)
signal.signal(signal.SIGHUP, gotsignal)

logger.info('Starting graphd version ' + str(static.major) + '.' + str(static.minor))

repo = repository.Repository(static.path, system.lower(), static.ttl)
loaded_plugins = repo.get_plugins()

if loaded_plugins:
	for p in loaded_plugins:
		p.start()
else:
	logger.error('No plugins found - bye')
	os.sys.exit(1)

def mgmt_list(conn, args):
	plist = ''

	for p in loaded_plugins:
		plist += p.id + ' '

	conn.wfile.write(plist)
	conn.wfile.write('\n')

def mgmt_fetch(conn, args):
	if args:
		plugin_id = args[0]

	conn.wfile.write(123456789)
	conn.wfile.write('\n')

def mgmt_help(conn, args):
	conn.wfile.write('commands:')

	for item in conn.server.cmds:
		conn.wfile.write(' ' + item[0])

	conn.wfile.write('\n')

server = tcp.ThreadedServer(('', 8090), tcp.RequestHandler)

server.add_callback('list', mgmt_list)
server.add_callback('fetch', mgmt_fetch)
server.add_callback('help', mgmt_help)

server.serve()
