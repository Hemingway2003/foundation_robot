#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re

import requests

stock_url_head = 'http://hq.sinajs.cn/list='

float_scale = '%.2f'

class SinaStockData(object):
	"""docstring for SinaStockData"""

	def _get_null_data(self, para):
		self.stock_name = 'null'
		self.today_open_price = 'null'
		self.yestoday_close_price = 'null'
		self.current_price = 'null'
		self.today_highest_price = 'null'
		self.today_lowest_price = 'null'
		# self.buy_one_price = stock_datas[6]
		# self.sell_one_price = stock_datas[7]
		self.total_bargain_number = 'null'
		self.total_bargain_price = 'null'
		self.date = 'null'
		self.current_percent = 'null'

	def __init__(self):
		self.stock_code = 'null'
		self._get_null_data(self)


	def get_stock_by_code(self, stock_code):
		stock_url = stock_url_head + stock_code
		self.stock_code = stock_code
		try:
			stock_page = requests.get(stock_url)
			# Request status judge
			if stock_page.status_code != 200:
				print("Get stock url failed")
				self._get_null_data(self)
				
			# print(stock_page.text)
		except requests.RequestException as e:
			self._get_null_data(self)

		try:
			# Get the data between two quotes
			# var hq_str_sh000001="上证指数,3379.3867,3383.3222,3389.0370,3404.6012,3369.0378,0,0,177462519,231979505279,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2020-07-13,10:09:16,00,";
			stock_factor = re.compile(r'["](.*)["]', re.S)
			stock_real_data = re.findall(stock_factor, stock_page.text)

			# Spilt datas
			stock_datas = stock_real_data[0].split(',')
			# print(stock_datas)
			# print(len(stock_datas))
			
			self.stock_name = stock_datas[0]
			self.today_open_price = stock_datas[1]
			self.yestoday_close_price = stock_datas[2]
			self.current_price = stock_datas[3]
			self.today_highest_price = stock_datas[4]
			self.today_lowest_price = stock_datas[5]
			# self.buy_one_price = stock_datas[6]
			# self.sell_one_price = stock_datas[7]
			self.total_bargain_number = stock_datas[8]
			self.total_bargain_price = stock_datas[9]
			if len(stock_datas) == 33:
				self.date = stock_datas[len(stock_datas) - 3] + ' ' + stock_datas[len(stock_datas) - 2]
			elif len(stock_datas) == 34:	
				self.date = stock_datas[len(stock_datas) - 4] + ' ' + stock_datas[len(stock_datas) - 3]
			current_percent_f = (float(self.current_price) - float(self.yestoday_close_price)) / float(self.yestoday_close_price) * 100
			self.current_percent = str(float_scale %current_percent_f)

			# print(self.current_price + ' ' + self.today_lowest_price + ' ' + self.current_percent)# + str(self.current_price / self.today_lowest_price))

			
		except Exception as e:
			self._get_null_data(self)




if __name__ == '__main__':
	print("Testing this module...")
	test = SinaStockData()
	test.get_stock_by_code("sz399006")
	# fund_result = get_fund_by_code_num("000001")
	# print(test.fund_code)
	# print(test.fund_estimated_date)
