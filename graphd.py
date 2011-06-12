import os
import time
import signal

import util
import repository

def gotsignal(signum, frame):
	if signum == signal.SIGINT:
		logger.info('Received interrupt signal - bye')
		os.sys.exit(0)
	if signum == signal.SIGHUP:
		logger.info('Reloading plugin directory')
		repo.reload_plugins()

path = 'plugins'
loglevel = 'debug'

logger = util.logger(loglevel)
system = os.uname()[0]

signal.signal(signal.SIGINT, gotsignal)
signal.signal(signal.SIGHUP, gotsignal)

logger.info('You are running ' + system)

repo = repository.Repository(path, system.lower())

# Setup TCP port and create CMD callbacks
#
# mgmt = tcp.listen('', 8090)
# mgmt.callback('list', list_plugins)

loaded_plugins = repo.get_plugins()

if loaded_plugins:
	for p in loaded_plugins:
		p.start()
else:
	logger.error('No plugins found - bye')
	os.sys.exit(1)

while True:
	time.sleep(1)
