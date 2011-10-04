import os
import re
import time
import logging
import subprocess

import ttimer
import static
import datastore

class Plugin:
	def __init__(self, file, plugin_path, ttl):
		self.file = file			# linux/cpu.sh
		self.name = file.rpartition('/')[2]	# cpu.sh

		self.plugin_path = plugin_path

		self.running = False
		self.logger = logging.getLogger('default')
		self.datastore = datastore.datastore(ttl)

		# Set default values
		self.interval = 10

		# Create thread with timer
		self.t = ttimer.ttimer(self.interval, self.execute)

	def start(self):
		self.logger.debug('Start polling ' + self.file + ' with interval ' + str(self.interval))
		self.running = True
		self.execute()
		self.t.start()

	def stop(self):
		self.logger.info('Stop polling ' + self.file)
		self.running = False
		self.t.stop()

	def status(self):
		return self.running

	def execute(self, args = None):
		self.logger.debug('Running ' + self.file)

		try:
			start = time.time()
        	
			proc = subprocess.Popen(
				[self.plugin_path + '/' + self.file],
				stdout = subprocess.PIPE,
				stderr = subprocess.PIPE
			)

			successful = False
			stdout, stderr = proc.communicate()

			if proc.returncode is 0:
				for line in stdout.split('\n'):
					match = re.match(r'^([^ ]+)\.value (.+)$', line)
					if line and match:
						self.datastore.push(match.groups()[0], match.groups()[1])
						successful = True

				if not successful:
					self.logger.warn('No valid output from ' + self.file)
			else:
				self.logger.error('Plugin returned with failure: exit code ' + proc.returncode)

			elapsed = time.time() - start

			# Warn if execution takes more time than the interval	
			if elapsed > self.interval:
				self.logger.warn('Execution of plugin exceeds interval (interval: ' + str(self.interval) + ' execution: ' + str(round(elapsed)) + ': ' + self.file)
        	
		except OSError:
			self.logger.error('Failed to execute plugin: ' + self.file)

	def update_interval(self, new_interval):
		self.t.update_interval(new_interval)
