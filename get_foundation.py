#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re

import requests

fund_url_head = "http://fundgz.1234567.com.cn/js/"
fund_url_tail = ".js"


class FoundationData(object):
	"""docstring for foundation_data"""
	def __init__(self):
		# super(foundation_data, self).__init__()
		self.fund_code = 0
		self.fund_name = 0
		self.fund_net_value_date = 0
		self.fund_unit_net_value = 0
		self.fund_estimated_value = 0
		self.fund_estimated_percent = 0
		self.fund_estimated_date = 0

	def get_fund_by_code_num(self, code_num):
		# Get main url
		fund_url = fund_url_head + code_num + fund_url_tail
		# Url request
		fund_page = requests.get(fund_url)

		try:
			# Request status judge
			if fund_page.status_code != 200:
				print("Get fund url failed")
				self.fund_code = 0
				self.fund_name = 0
				self.fund_net_value_date = 0
				self.fund_unit_net_value = 0
				self.fund_estimated_value = 0
				self.fund_estimated_percent = 0
				self.fund_estimated_date = 0
			# print(fund_page.text)
		except requests.RequestException as e:
			self.fund_code = 0
			self.fund_name = 0
			self.fund_net_value_date = 0
			self.fund_unit_net_value = 0
			self.fund_estimated_value = 0
			self.fund_estimated_percent = 0
			self.fund_estimated_date = 0

		# Get the data between two bracket
		found_factor = re.compile(r'[{](.*)[}]', re.S)
		fund_real_data = re.findall(found_factor, fund_page.text)

		# Spilt datas
		fund_datas = fund_real_data[0].split(',')

		# Get rid of quotes
		found_quotes = re.compile(r'["](.*)["]', re.S)

		self.fund_code = re.findall(found_quotes, fund_datas[0].split(":")[1])[0]
		self.fund_name = re.findall(found_quotes, fund_datas[1].split(":")[1])[0]
		self.fund_net_value_date = re.findall(found_quotes, fund_datas[2].split(":")[1])[0]
		self.fund_unit_net_value = re.findall(found_quotes, fund_datas[3].split(":")[1])[0]
		self.fund_estimated_value = re.findall(found_quotes, fund_datas[4].split(":")[1])[0]
		self.fund_estimated_percent = re.findall(found_quotes, fund_datas[5].split(":")[1])[0]
		self.fund_estimated_date = re.findall(found_quotes, fund_datas[6].split(":")[1] + ':' + fund_datas[6].split(":")[2])[0]

if __name__ == '__main__':
	print("Testing this module...")
	test = FoundationData()
	test.get_fund_by_code_num("000001")
	# fund_result = get_fund_by_code_num("000001")
	# print(test.fund_code)
	# print(test.fund_estimated_date)
