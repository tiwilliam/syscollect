import os
import time
import subprocess

import util
import mgmt
import repository

path = 'plugins'
loglevel = 'debug'

logger = util.logger(loglevel)
repo = repository.Plugins(path)

mgmt_server = mgmt.MGMT('', 8090)
mgmt_server.start(mgmt.MGMTHandler)

for p in repo.get_plugins():
	p.start()

while True:
	time.sleep(10)
	for p in repo.get_plugins():
		if p.path == 'cpu.sh':
			p.update_interval(10)

mgmt_server.shutdown()
