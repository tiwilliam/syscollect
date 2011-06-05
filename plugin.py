import ttimer
import logging

class Plugin():
	def __init__(self, path, config):
		self.path = path
		self.config = config
		self.logger = logging.getLogger('default')

		self.interval = 10
		self.title = None
		self.subtitle = None

	def start(self):
		self.config = self.parse_config(self.config)

		self.logger.debug('Starting thread for ' + self.path)
		self.t = ttimer.ttimer(self.interval, -1, self.execute, self.path)
		self.t.start()

	def execute(self, path):
		print path

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
					print 'Unknown config property: ' + var
