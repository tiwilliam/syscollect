import re
import os
import ttimer
import logging
import subprocess

import plugin

class Repository():
	def __init__(self, path):
		self.path = path
		self.logger = logging.getLogger('default')
		self.load_plugins()

	def load_plugins(self):
		files = os.listdir(self.path)
		self.plugins = []

		for file in files:
			full_file_path = self.path + '/' + file

			p = re.compile('^[^\.]')
			if p.match(file) and os.path.isfile(full_file_path):
				self.logger.debug('Loading plugin ' + file)

				proc = subprocess.Popen(
					[full_file_path, 'config'],
					stdout = subprocess.PIPE,
					stderr = subprocess.PIPE
				)

				stdout, stderr = proc.communicate()

				config = stdout.strip()
				config_list = config.split('\n')

				self.plugins += [plugin.Plugin(file, config_list)]

		self.logger.info('Loaded ' + str(len(self.plugins)) + ' plugins from ' + self.path)

		return self.plugins

	def load_saved_config(self):
		return # Do overrides to config values

	def get_plugins(self):
		return self.plugins
