#!/usr/bin/python

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

def addsignal(signum, func):
	try:
		signal.signal(signum, func)
	except ValueError:
		logger.warn('Signal not supported in ' + static.system + ': ' + str(signum))

def gotsignal(signum, frame):
	if signum == 2: # SIGINT
		logger.info('Received interrupt signal - bye')
		sys.exit(0)

## TCP MGMT functions ##################################################

def mgmt_list(conn, args):
	host = conn.client_address[0]
	port = str(conn.client_address[1])
	logger.info(host + ':' + port + ' - Listing plugins')

	list = []

	for p in loaded_plugins:
		list += [p.file]

	data = json.dumps(list)
	conn.wfile.write(data + '\n')

# Fetch data for specified plugin
def mgmt_fetch(conn, args):
	host = conn.client_address[0]
	port = str(conn.client_address[1])

	try:
		logger.info(host + ':' + port + ' - Fetching plugin data')

		fetch_id = args[0]
		fetch_plugin = repo.get_plugin(fetch_id)

		# Could not find plugin
		if not fetch_plugin:
			conn.wfile.write('no such plugin: ' + fetch_id + '\n')
			throw

		if len(args) == 1:
			# Fetch all history we have
			data = json.dumps(fetch_plugin.datastore.data)
		elif len(args) == 2:
			fetch_offset = int(args[1])
			if fetch_offset:
				# Fetch history from offset specified
				ret_data = {}
				# Loop plugin values
				for k in fetch_plugin.datastore.data:
					ret_data[k] = []
					# Loop each timestamp
					for ts in fetch_plugin.datastore.data[k]:
						# Get rid of data before our timestamp
						if int(ts[0]) > fetch_offset:
							ret_data[k] += [ts]
			else:
				# Fetch latest value
				ret_data = {}
				# Loop plugin values
				for k in fetch_plugin.datastore.data:
					list_len = len(fetch_plugin.datastore.data[k])
					ret_data[k] = fetch_plugin.datastore.data[k][list_len - 1]

			data = json.dumps(ret_data)
		else:
			throw

		conn.wfile.write(data + '\n')
	except:
		logger.info(host + ':' + port + ' - Failed fetching plugin data')
		conn.wfile.write('usage: fetch <plugin id> [<uptime offset>]\n')

# List all commands
def mgmt_help(conn, args):
	conn.wfile.write('commands:')

	for item in conn.server.cmds:
		conn.wfile.write(' ' + item[0])

	conn.wfile.write('\n')

## Main program ########################################################

logger = util.logger(static.loglevel)

addsignal(2, gotsignal) # SIGINT

logger.info('Starting ' + static.name + ' version ' + static.version + ' (' + static.fqdn + ')')

repo = repository.Repository()
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
server.add_callback('help', mgmt_help)

server.serve()
