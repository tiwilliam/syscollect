import sys
import time
import thread

class ttimer:
	def __init__(self, interval, cbfunc, cbparam=[]):
		self.running = True
		self.interval = interval

		thread.start_new_thread(self._callback, (cbfunc, cbparam))

	def start(self):
		self.running = True

	def stop(self):
		self.running = False

	def status(self):
		if self.running:
			return True
		else:
			return False

	def update_interval(self, new_interval):
		self.interval = new_interval

	def _callback(self, cbfunc, cbparam=[]):
		time.sleep(self.interval)

		while True:
			if self.running:
				s = time.time()
				cbfunc(cbparam)
				d = time.time() - s
				time.sleep(self.interval - d)
			else:
				break

		self.running = False
