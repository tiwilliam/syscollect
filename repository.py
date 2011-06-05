import re
import os
import ttimer
import logging
import subprocess

import plugin

class Repository():
	def __init__(self, path, system):
		self.path = path
		self.system = system
		self.logger = logging.getLogger('default')
		self.load_plugins()

	def reload_plugins(self):
		old_list = self.get_plugins()
		self.load_plugins()
		new_list = self.get_plugins()

		old_ids = []
		new_ids = []

		for old in old_list:
			old_ids += [old.id]

		for new in new_list:
			new_ids += [new.id]

		removed_plugins = set(old_ids) - set(new_ids)
		added_plugins = set(new_ids) - set(old_ids)

	def load_plugins(self):
		try:
			files = os.listdir(self.path)
			self.plugins = []

			for file in files:
				full_file_path = self.path + '/' + file

				p = re.compile('^[^\.]')
				if p.match(file) and os.path.isfile(full_file_path):
					try:
						proc = subprocess.Popen(
							[full_file_path, 'config'],
							stdout = subprocess.PIPE,
							stderr = subprocess.PIPE
						)

						stdout, stderr = proc.communicate()

						config = stdout.strip()
						config_list = config.split('\n')

						try:
							self.plugins += [plugin.Plugin(file, config_list)]
						except plugin.PluginError as e:
							self.logger.error(e)

					except OSError as e:
						self.logger.warn('Failed to fetch config: ' + self.path + '/' + file + ': ' + e.strerror)

			self.logger.info('Loaded ' + str(len(self.plugins)) + ' plugins from ' + self.path)

			return self.plugins
		except OSError as e:
			self.logger.error('Failed to read directory \'' + self.path + '\': ' + e.strerror)
			return None

	def load_saved_config(self):
		return # Do overrides to config values

	def get_plugins(self):
		if hasattr(self, 'plugins'):
			return self.plugins
		else:
			return None
