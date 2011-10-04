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
		self.system = static.system.lower()
		self.logger = logging.getLogger('default')
		self.plugins = []
		
		self.load_plugins(self.system)
		self.load_plugins('noarch')

	def pop_plugin(self, id):
		i = 0
		for p in self.plugins:
			if p.file == id:
				return self.plugins.pop(i)
			i += 1

	def get_plugin(self, id):
		i = 0
		for p in self.plugins:
			if p.name == id:
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
					if self.exists(file):
						self.logger.warn('Ignoring ' + file + ': conflicting plugin name')
					else:
						new_plug = plugin.Plugin(file, self.plug_path, self.ttl)
						self.plugins += [new_plug]
				except ValueError as e:
					self.logger.error(file + ': Failed to load plugin: ' + str(e))

		self.logger.info('Loaded plugins from ' + self.plug_path + '/' + arch)

		return self.plugins

	def exists(self, file):
		for x in self.plugins:
			if x.name == file.rpartition('/')[2]:
				return True

		return False
