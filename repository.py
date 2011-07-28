import re
import os
import ttimer
import logging
import subprocess

import plugin
import static

class Repository:
	def __init__(self):
		self.ttl = static.ttl
		self.plug_path = static.plug_path
		self.conf_path = static.conf_path
		self.system = static.system.lower()
		self.logger = logging.getLogger('default')
		
		self.load_plugins('noarch')
		self.load_plugins(self.system)

	def pop_plugin(self, id):
		i = 0
		for p in self.plugins:
			if p.file == id:
				return self.plugins.pop(i)
			i += 1

	def get_plugin(self, id):
		i = 0
		for p in self.plugins:
			if p.file == id:
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

	def read_plugdir(self, arch):
		try:
			files = os.listdir(self.plug_path + '/' + arch)
			plugins = []

			for file in files:
				full_file_path = self.plug_path + '/' + arch + '/' + file

				if os.path.isfile(full_file_path):
					plugins += [arch + '/' + file]

			return plugins
		except OSError as e:
			self.logger.error('Failed to read directory \'' + self.plug_path + '/' + arch + '\': ' + e.strerror)
			return None
		

	def load_plugins(self, arch):
		files = self.read_plugdir(arch)
		self.plugins = []

		if files:
			for file in files:
				ignoresuffix = "|".join(static.ignoresuffix)

				dotfile = re.compile('^\.')
				ignore = re.compile('\.(' + ignoresuffix + ')$')

				# Skip dot files and file extensions listed in static.ignoresuffix
				if dotfile.search(file) or ignore.search(file):
					self.logger.debug('Skipping file: ' + file)
					continue

				try:
					new_plug = plugin.Plugin(file, self.plug_path, self.conf_path, self.ttl)
					self.plugins += [new_plug]
				except ValueError as e:
					self.logger.error(file + ': Failed to load plugin: ' + str(e))

		self.logger.info('Loaded ' + str(len(self.plugins)) + ' plugins from ' + self.plug_path + '/' + arch)

		return self.plugins

	def config_load(self):
		return # Do overrides to config values

	def config_save(self):
		return # Save runtime config to file
