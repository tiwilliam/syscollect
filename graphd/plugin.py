import os
import re
import time
import logging
import subprocess

import ttimer
import static
import datastore

class Plugin:
	def __init__(self, file, plug_path, ttl):
		self.file = file		# linux/graph_cpu
		self.plug_path = plug_path	# /etc/graphd/plug

		self.running = False
		self.logger = logging.getLogger('default')
		self.datastore = datastore.datastore(ttl)

		# Set default values
		self.interval = 10

		# Detect plug type
		file_split = self.file.split('/')
		plug_name = file_split[len(file_split) - 1]
		plug_type = plug_name.split('_')[0]

		# Get rid of file extension
		self.filenoext = os.path.splitext(self.file)[0]

		if plug_type in static.types:
			self.type = plug_type
		else:
			raise ValueError, 'Invalid plugin type'

		# Override defaults with values from plugin
		if self.plug_path and self.file:
			self.config = self.read_config()

		# Create thread with timer
		self.t = ttimer.ttimer(self.interval, self.execute)

	def read_config(self):
		file_path = self.plug_path + '/' + self.filenoext + '.conf'

		try:
			f = open(file_path, "r")
			text = f.read()
			f.close()

			config = text.strip()
			config_list = config.split('\n')

			return self.parse_config(config_list)

		except (OSError, IOError) as e:
			self.logger.error('Failed to get config: ' + file_path + ': ' + e.strerror)
			return None

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
				[self.plug_path + '/' + self.file],
				stdout = subprocess.PIPE,
				stderr = subprocess.PIPE
			)

			successful = False
			stdout, stderr = proc.communicate()

			if proc.returncode is 0:
				for line in stdout.split('\n'):
					match = re.match(r'^([^ ]+) (.+)$', line)
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

	def parse_config(self, config):
		for prop in config:
			prop = prop.strip().replace('\t', ' ')
			prop_tuple = prop.partition(' ')
			if len(prop) >= 2:
				var = prop_tuple[0]
				val = prop_tuple[2].strip()

				if var == 'interval':
					self.interval = int(val)
				else:
					self.logger.warn(self.file + ': Unknown config property: ' + var)
