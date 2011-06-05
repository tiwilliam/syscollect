import os
import time
import subprocess

import util
import repository

path = 'plugins'
loglevel = 'debug'

logger = util.logger(loglevel)
repo = repository.Repository(path)

# Setup TCP port and create CMD callbacks
#
# mgmt = tcp.listen('', 8090)
# mgmt.callback('list', list_plugins)

for p in repo.get_plugins():
	p.start()

while True:
	time.sleep(10)
