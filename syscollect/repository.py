import re
import os
import logging

import plugin
import static


class Repository:
    def __init__(self):
        self.ttl = static.ttl
        self.system = static.system.lower()
        self.logger = logging.getLogger('default')
        self.plugins = []

        for path in static.plugin_paths:
            if not os.path.isdir(path):
                continue
            self.plugin_path = path

        if not self.plugin_path:
            raise RuntimeError('Could not find plugin directory')

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
            if not p.status():
                p.start()

    def read_plugdir(self, arch):
        plugins = []
        try:
            files = os.listdir(self.plugin_path + '/' + arch)
            for file in files:
                full_file_path = self.plugin_path + '/' + arch + '/' + file

                if os.path.isfile(full_file_path):
                    plugins += [arch + '/' + file]
        except OSError as e:
            params = (self.plugin_path, arch, e.strerror)
            raise Exception('Failed to read directory %s/%s: %s' % params)

        return plugins

    def load_plugins(self, arch):
        files = self.read_plugdir(arch)

        if not files:
            return self.plugins

        for file in files:
            ignoresuffix = "|".join(static.ignoresuffix)

            dotfile = re.compile('^\.')
            ignore = re.compile('\.(' + ignoresuffix + ')$')

            # Skip dot files and file extensions (static.ignoresuffix)
            if dotfile.search(file) or ignore.search(file):
                self.logger.warn('Skipping file: ' + file)
                continue

            try:
                if self.exists(file):
                    raise ValueError('Conflicting name')
                new_plug = plugin.Plugin(file, self.plugin_path, self.ttl)
                self.plugins += [new_plug]
            except ValueError as e:
                self.logger.error(file + ': Failed to load plugin: ' + str(e))

        self.logger.info('Loaded plugins from ' + self.plugin_path + '/' + arch)
        return self.plugins

    def exists(self, file):
        for x in self.plugins:
            if x.name == file.rpartition('/')[2]:
                return True

        return False
