import sys
import time
import thread

class ttimer():
	def __init__(self, interval, retry, cbfunc, cbparam=[]):
		self.is_start = False
		self.is_end = False
		self.interval = interval

		thread.start_new_thread(self._callback, (retry, cbfunc, cbparam))

	def start(self):
		self.mytime = time.time()
		self.is_start = True
		self.is_end = False

	def stop(self):
		self.mytime = time.time()
		self.is_start = False
		self.is_end = True

	def is_stop(self):
		if self.is_end:
			return True
		else:
			return False

	def update_interval(self, new_interval):
		self.interval = new_interval

	def _callback(self, retry, cbfunc, cbparam=[]):
		self.retry = retry
		retry = 0

		if self.is_end:
			return None

		while True:
			if self.is_end:
				break

			if self.retry == -1:
				pass
			elif retry >= self.retry:
				break

			if self.is_start:
				tmptime = time.time()

				if tmptime >= (self.mytime + self.interval):
					cbfunc(cbparam)
					self.mytime = time.time()
					retry += 1
				else:
					pass

				time.sleep(0.1)

		self.is_end = True
