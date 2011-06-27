import sys
import time
import signal

import tcp
import util
import static
import repository

try:
	import simplejson as json
except ImportError:
	import json

## Signal handler ######################################################

def gotsignal(signum, frame):
	if signum == signal.SIGINT:
		logger.info('Received interrupt signal - bye')
		sys.exit(0)
	if signum == signal.SIGHUP:
		logger.info('Reloading plugin directory')
		repo.reload_plugins()

## TCP MGMT functions ##################################################

def mgmt_list(conn, args):
	host = conn.client_address[0]
	port = str(conn.client_address[1])
	logger.info(host + ':' + port + ' - Listing all plugins')

	plist = ''

	for p in loaded_plugins:
		plist += p.id + ' '

	conn.wfile.write(plist.rstrip())
	conn.wfile.write('\n')

# Fetch data for specified plugin
def mgmt_fetch(conn, args):
	host = conn.client_address[0]
	port = str(conn.client_address[1])

	try:
		logger.info(host + ':' + port + ' - Fetching plugin data')

		# Fetch all history we have
		if len(args) == 1:
			fetch_id = args[0]
			fetch_plugin = repo.get_plugin(fetch_id)
			if fetch_plugin:
				data = json.dumps(fetch_plugin.datastore.data)
				conn.wfile.write(data + '\n')
			else:
				conn.wfile.write('no such plugin: ' + fetch_id + '\n')
		# Fetch history from offset specified
		elif len(args) == 2:
			fetch_id = args[0]
			fetch_offset = int(args[1])
			fetch_plugin = repo.get_plugin(fetch_id)

			if fetch_plugin:
				ret_data = {}
				# Loop plugin values
				for k in fetch_plugin.datastore.data:
					ret_data[k] = []
					# Loop each timestamp
					for ts in fetch_plugin.datastore.data[k]:
						# Get rid of data before our timestamp
						if int(ts[0]) > fetch_offset:
							ret_data[k] += [ts]

				data = json.dumps(ret_data)
				conn.wfile.write(data + '\n')
			else:
				conn.wfile.write('no such plugin: ' + fetch_id + '\n')
		else:
			throw
	except:
		logger.info(host + ':' + port + ' - Failed fetching plugin data')
		conn.wfile.write('usage: fetch <plugin id> [<uptime offset>]\n')

# List all commands
def mgmt_help(conn, args):
	conn.wfile.write('commands:')

	for item in conn.server.cmds:
		conn.wfile.write(' ' + item[0])

	conn.wfile.write('\n')

# Reload plugin directory
def mgmt_reload(conn, args):
	host = conn.client_address[0]
	port = str(conn.client_address[1])
	logger.info(host + ':' + port + ' - Reloading plugin directory')

	repo.reload_plugins()

## Main program ########################################################

logger = util.logger(static.loglevel)

signal.signal(signal.SIGINT, gotsignal)
signal.signal(signal.SIGHUP, gotsignal)

logger.info('Starting ' + static.name + ' version ' + static.version + ' (' + static.fqdn + ')')

repo = repository.Repository(static.path)
loaded_plugins = repo.get_plugins()

if loaded_plugins:
	for p in loaded_plugins:
		p.start()
else:
	logger.error('No plugins found - bye')
	sys.exit(1)

server = tcp.ThreadedServer(('', 8090), tcp.RequestHandler)

server.add_callback('list', mgmt_list)
server.add_callback('fetch', mgmt_fetch)
server.add_callback('reload', mgmt_reload)
server.add_callback('help', mgmt_help)

server.serve()
