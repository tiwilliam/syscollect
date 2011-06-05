import os
import re
import ttimer
import logging

class Plugin():
	def __init__(self, path, config):
		self.path = path
		self.filename = os.path.splitext(path)[0]
		self.config = config
		self.logger = logging.getLogger('default')

		m = re.match(r'([\w\d.]+)-([\w\d.]+)-([\d.]+)-([\w\d.]+)', self.filename)

		try:
			self.name = m.group(1)
			self.author = m.group(2)
			self.version = m.group(3)
			self.os = m.group(4)
			self.id = self.name + '-' + self.author + '-' + self.os
		except:
			raise PluginError('Invalid plugin name: ' + self.path)

		self.interval = 10
		self.title = None
		self.subtitle = None

	def start(self):
		self.config = self.parse_config(self.config)

		self.logger.debug('Start polling \'' + self.name + '\' version ' + self.version)
		self.t = ttimer.ttimer(self.interval, -1, self.execute, self.path)
		self.t.start()

	def execute(self, path):
		self.logger.debug('Running ' + self.name)

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
				elif var == 'title':
					self.title = val
				elif var == 'subtitle':
					self.subtitle = val
				else:
					self.logger.warn('Unknown config property: ' + var)

class PluginError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return self.value
