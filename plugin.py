import os
import re
import logging
import subprocess

import ttimer

class Plugin():
	def __init__(self, file, path):
		self.id = file
		self.file = file
		self.path = path
		self.running = False
		self.logger = logging.getLogger('default')

		# Parse plugin name, author and os
		m = re.match(r'([\w\d.]+)-([\w\d.]+)-([\w\d.]+)', os.path.splitext(file)[0])

		try:
			self.name = m.group(1)
			self.author = m.group(2)
			self.os = m.group(3)
		except:
			raise PluginError('Invalid plugin name: ' + self.file)

		# Set default values
		self.interval = 10

		# Override defaults with values from plugin
		if self.path and self.file:
			self.config = self.read_config()

		# Create thread with timer
		self.t = ttimer.ttimer(self.interval, -1, self.execute, self.file)

	def read_config(self):
		file_path = self.path + '/' + self.file

		try:
			proc = subprocess.Popen(
				[file_path, 'config'],
				stdout = subprocess.PIPE,
				stderr = subprocess.PIPE
			)

			stdout, stderr = proc.communicate()

			config = stdout.strip()
			config_list = config.split('\n')

			return self.parse_config(config_list)

		except OSError as e:
			self.logger.error('Failed to get config: ' + file_path + ': ' + e.strerror)

			return None


	def start(self):
		self.logger.debug('Start polling ' + self.id)
		self.running = True
		self.t.start()

	def stop(self):
		self.logger.info('Stop polling ' + self.id)
		self.running = False
		self.t.stop()

	def status(self):
		return self.running

	def execute(self, path):
		self.logger.debug('Running ' + self.id + ' (' + str(self) + ')')

	def update_interval(self, new_interval):
		self.t.update_interval(new_interval)

	def parse_config(self, config):
		for prop in config:
			prop = prop.split(' ')
			if len(prop) >= 2:
				var = prop[0]
				val = prop[1]

				if var == 'interval':
					self.interval = int(val)
				#elif var == 'title':
				#	self.title = val
				else:
					self.logger.warn('Unknown config property: ' + var)

class PluginError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return self.value
