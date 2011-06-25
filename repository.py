import re
import os
import ttimer
import logging
import subprocess

import plugin
import static

class Repository():
	def __init__(self, path):
		self.ttl = static.ttl
		self.path = path
		self.system = static.system.lower()
		self.logger = logging.getLogger('default')
		
		self.load_plugins(self.path + '/noarch')
		self.load_plugins(self.path + '/' + self.system)

	def pop_plugin(self, id):
		i = 0
		for p in self.plugins:
			if p.id == id:
				return self.plugins.pop(i)
			i += 1

	def get_plugin(self, id):
		i = 0
		for p in self.plugins:
			if p.id == id:
				return p
			i += 1

		return None

	def get_plugins(self):
		if hasattr(self, 'plugins'):
			return self.plugins

		return None

	def start_plugins(self):
		for p in self.plugins:
			if not p.status(): p.start()

	def reload_plugins(self):
		old_ids = []
		new_ids = []

		# Build up lists with identifers before and after reload
		for new in self.read_dir(self.path + '/noarch'):
			new_ids += [new]
		
		for new in self.read_dir(self.path + '/' + self.system):
			new_ids += [new]

		for old in self.get_plugins():
			old_ids += [old.id]

		removed_plugins = set(old_ids) - set(new_ids)
		added_plugins = set(new_ids) - set(old_ids)

		# Stop threads for plugins that have been removed
		for p in removed_plugins:
			old_plugin = self.pop_plugin(p)
			if old_plugin:
				old_plugin.stop()
				del old_plugin

		# Add new plugins to list
		for p in added_plugins:
			self.logger.info('Adding ' + p + ' to polling list')
			self.plugins += [plugin.Plugin(p, self.path, self.ttl)]

		# Start stopped plugins
		self.start_plugins()

	def read_dir(self, plugin_path):
		try:
			files = os.listdir(plugin_path)
			plugins = []

			for file in files:
				full_file_path = plugin_path + '/' + file

				if os.path.isfile(full_file_path):
					dotfile = re.compile('^\.')
					srcfile = re.compile('\.c$')

					# Skip files
					if dotfile.search(file) or srcfile.search(file):
						self.logger.debug('Skipping file: ' + file)
						continue

					plugins += [self.system + '/' + file]

			return plugins
		except OSError as e:
			self.logger.error('Failed to read directory \'' + plugin_path + '\': ' + e.strerror)
			return None
		

	def load_plugins(self, path):
		files = self.read_dir(path)
		self.plugins = []

		if files:
			for file in files:
				try:
					self.plugins += [plugin.Plugin(file, self.path, self.ttl)]
				except plugin.PluginError as e:
					self.logger.error(e)

		self.logger.info('Loaded ' + str(len(self.plugins)) + ' plugins from ' + path)

		return self.plugins

	def config_load(self):
		return # Do overrides to config values

	def config_save(self):
		return # Save runtime config to file
