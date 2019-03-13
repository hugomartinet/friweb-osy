from datetime import datetime

from tools.Color import Color

class TimeCounter:

	def __init__(self):
		self.begin = 0
		self.end = 0

	def start(self):
		self.begin = datetime.now()

	def stop(self):
		self.end = datetime.now()

	def stop_and_print(self):
		self.stop()
		delta = self.end - self.begin
		seconds = delta.seconds
		micro = delta.microseconds
		print(Color.PURPLE + str(seconds + micro/1000000) + ' seconds\n' + Color.END)
		
	