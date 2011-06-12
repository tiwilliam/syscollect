import os
import re
import time
import logging
import subprocess

import ttimer

class Plugin():
	def __init__(self, file, path):
		self.id = os.path.splitext(file)[0]
		self.file = file
		self.path = path
		self.running = False
		self.logger = logging.getLogger('default')
		self.data = {}

		# Parse plugin name, author and os
		# loadavg-william-linux.sh
		m = re.match(r'([\w\d.]+)-([\w\d.]+)-([\w\d.]+)', os.path.splitext(file)[0])

		try:
			self.name = m.group(1)
			self.author = m.group(2)
			self.os = m.group(3)
		except:
			raise PluginError('Invalid plugin name: ' + self.file + ': expected <name>-<author>-<os>.<ext>')

		# Set default values
		self.interval = 10

		# Override defaults with values from plugin
		if self.path and self.file:
			self.config = self.read_config()

		# Create thread with timer
		self.t = ttimer.ttimer(self.interval, self.execute)

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
		self.logger.debug('Start polling ' + self.id + ' with interval ' + str(self.interval))
		self.running = True
		self.t.start()

	def stop(self):
		self.logger.info('Stop polling ' + self.id)
		self.running = False
		self.t.stop()

	def status(self):
		return self.running

	def execute(self, args):
		self.logger.debug('Running ' + self.id)

		try:
			start = time.time()
        	
			proc = subprocess.Popen(
				[self.path + '/' + self.file],
				stdout = subprocess.PIPE,
				stderr = subprocess.PIPE
			)
        	
			stdout, stderr = proc.communicate()

			key = None
			value = None

			for line in stdout.split('\n'):
				if line:
					# Save value in dict
					match = re.match(r'(.*)\.value ([\d.]+)$', line)

					if match:
						key = match.groups()[0]
						value = match.groups()[1]

						if key in self.data:
							self.data[key] += [value]
						else:
							self.data[key] = [value]

			if key is None:
				self.logger.warn('No valid data output from ' + self.id)
        	
			elapsed = time.time() - start
		
			# Warn if execution takes more time than the interval	
			if elapsed > self.interval:
				self.logger.warn('Execution of plugin exceeds interval (interval: ' + str(self.interval) + ' execution: ' + str(round(elapsed)) + ': ' + self.id)
        	
		except OSError:
			self.logger.error('Failed to execute plugin: ' + self.id)

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
