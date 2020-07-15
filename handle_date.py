#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime


class DateTimeNow(object):
	"""docstring for DateTimeObj"""
	def __init__(self):
		self.now = datetime.datetime.now()

	def get_weekday(self):
		# self.weekday = datetime.datetime(self.now.year, self.now.month, 6, 0, 0, 0).weekday()
		self.weekday = self.now.weekday()

		# if self.weekday == 0:
		# 	self.weekday = 1
		# else:
		# 	self.weekday+=1

		self.weekday += 1
		return self.weekday

	def get_passed_second(self):
		self.passed_sec = self.now.second + self.now.minute * 60 + self.now.hour * 3600
		return self.passed_sec

	def get_special_passed_second(self, hour, min, sec):
		self.special_passed_second = sec + min * 60 + hour * 3600
		return self.special_passed_second

		

if __name__ == '__main__':    
	print("Testing this module...")

	test = DateTimeNow()
	print(test.get_weekday())
	print(test.get_passed_second())
	print(test.get_special_passed_second(9,00,00))
	print(test.get_special_passed_second(15,10,00))
	
