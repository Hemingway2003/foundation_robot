#!/usr/bin/python
# -*- coding: UTF-8 -*-
import threading
import tkinter
import time

import handle_date

import get_foundation
import get_stock_data_from_sina

global main_ui, window_update_thread, update_event

# default_char_width = 11
# default_char_height = 21

default_title = 'Stock & Fund List'

default_up_color = 'red'
default_down_color = 'green'
default_unknow_color = 'grey'
default_split_color = 'yellow'

default_uptime = 600 #60 #600 # unit: second
default_fast_uptime = 6

extra_data_len = 30

max_window_height_line = 30


class MainWindow(object):
	"""docstring for MainWindow"""
	def __init__(self, tk, codes):
		global window_update_thread, main_ui
		# self.init = 0
		self.firstupdate = 0
		# super(MainWindow, self).__init__()
		# self.win_width = width
		# self.win_height = height
		
		# Basic tkinker setting
		self.win = tk #tkinter.Toplevel(tk)
		self.win.title(default_title)
		self.win.bind('<FocusIn>', self._focus)
		self.win.bind('<FocusOut>', self._unfocus)
		self.win.protocol("WM_DELETE_WINDOW", self._quit)
		self.win.grid_rowconfigure(0, weight=1)
		self.win.columnconfigure(0, weight=1)
		# self.win.overrideredirect(True)
		self.win.wm_attributes('-topmost',1)

		# Stock and fund
		self.stock = get_stock_data_from_sina.SinaStockData()
		self.fund = get_foundation.FoundationData()
		# self.fund.get_fund_by_code_num("110013")

		# Set window position
		sw = self.win.winfo_screenwidth()
		sh = self.win.winfo_screenheight()
		
		# self.win_x = (sw - width) / 2
		# self.win_y = (sh - height) / 2
		# self.win.geometry("%dx%d+%d+%d" %(self.win_width, self.win_height, self.win_x, self.win_y))


		# Basic frame
		self.basic_frame = tkinter.Frame(self.win)
		self.basic_frame.grid(row=2, column=0, pady=(5, 0), sticky='nw')
		self.basic_frame.grid_rowconfigure(0, weight=1)
		self.basic_frame.grid_columnconfigure(0, weight=1)
		# Set grid_propagate to False to allow 5-by-5 buttons resizing later
		self.basic_frame.grid_propagate(False)

		# Canvas
		canvas = tkinter.Canvas(self.basic_frame)
		canvas.grid(row=0, column=0, sticky="news")

		# Link a scrollbar to the canvas
		self.vsb = tkinter.Scrollbar(self.basic_frame, orient="vertical", command=canvas.yview)
		self.vsb.grid(row=0, column=1, sticky='ns')
		canvas.configure(yscrollcommand=self.vsb.set)

		# Create a frame to show the real elements
		self.show_frame = tkinter.Frame(canvas, bg="black")
		canvas.create_window((0, 0), window=self.show_frame, anchor='nw')

		# Showed labels
		self.labs = [tkinter.Label() for i in range(len(codes))]

		self.codes = codes
		i = 0
		for code in codes:
			code_type = code.split(',')[0]

			if 'split' == code_type:
				split_data = '-'
				for j in range(int(20)):
					split_data += '-'
				self.labs[i] = tkinter.Label(self.show_frame, fg = default_split_color, bg = 'black', text = split_data)
			else:
				self.labs[i] = tkinter.Label(self.show_frame, fg ='red', bg = 'black', text = 'null' + ' : ' + 'null' + ' (' + 'null' + ' %)' + '-' + 'null')
			self.labs[i].grid(row=i, column=0, sticky='news')
			i = i + 1

		# Update buttons frames idle tasks to let tkinter calculate buttons sizes
		self.show_frame.update_idletasks()
		self.labs_max_width = 0
		self.lab_max_height = 0
		for lab in self.labs:
			if self.labs_max_width < lab.winfo_width():
				self.labs_max_width = lab.winfo_width()
		if len(self.labs) > max_window_height_line:
			self.lab_max_height = max_window_height_line * self.labs[0].winfo_height()
		else:
			self.lab_max_height = len(self.labs) * self.labs[0].winfo_height()

		# Resize the canvas frame to show
		self.basic_frame.config(width=self.labs_max_width + self.vsb.winfo_width(),
		                    height=self.lab_max_height)

		# Set the canvas scrolling region
		canvas.config(scrollregion=canvas.bbox("all"))


	def _focus(self, event):
		self.win.attributes('-alpha', 1)

	def _unfocus(self, event):
		self.win.attributes('-alpha', 1)

	def _quit(self):
		global window_update_thread
		self.win.destroy()
		window_update_thread.exit()

	def update_labels(self):
		print("Update")
		if 1 == self.firstupdate:
			datedata = handle_date.DateTimeNow()
			if datedata.get_weekday() > 5:
				return
			if datedata.get_passed_second() < datedata.get_special_passed_second(9,20,0) or \
			(datedata.get_passed_second() > datedata.get_special_passed_second(11,40,0) and datedata.get_passed_second() < datedata.get_special_passed_second(13,20,0)) or \
			datedata.get_passed_second() > datedata.get_special_passed_second(15,10,0):
				return

		self.firstupdate = 1

		index = 0
		for code in self.codes:
			code_type = code.split(',')[0]
			real_code = code.split(',')[1]

			if 'split' != code_type:
				# Stock
				if 'stock' == code_type:
					self.stock.get_stock_by_code(real_code)

					if 'null' != self.stock.current_percent:
						percent = float(self.stock.current_percent)
						if percent < 0.0:
							color = default_down_color
						else:
							color = default_up_color
					else:
						color = default_unknow_color
					if 'null' == self.stock.stock_name:
						self.labs[index].config(fg = color, text = self.stock.stock_code + ' : ' + self.stock.current_price + 
						' (' + self.stock.current_percent + ' %)' + '-' + self.stock.date)
					else:
						self.labs[index].config(fg = color, text = self.stock.stock_name + ' : ' + self.stock.current_price + 
						' (' + self.stock.current_percent + ' %)' + '-' + self.stock.date)
				# Fund
				elif 'fund' == code_type:
					self.fund.get_fund_by_code_num(real_code)
					if 'null' != self.fund.fund_estimated_percent:
						percent = float(self.fund.fund_estimated_percent)
						if percent < 0.0:
							color = default_down_color
						else:
							color = default_up_color
					else:
						color = default_unknow_color
					if 'null' == self.fund.fund_name:
						self.labs[index].config(fg = color, text = self.fund.fund_code + ' : ' + self.fund.fund_estimated_value + 
						' (' + self.fund.fund_estimated_percent + ' %)' + '-' + self.fund.fund_estimated_date)
					else:
						self.labs[index].config(fg = color, text = self.fund.fund_name + ' : ' + self.fund.fund_estimated_value + 
						' (' + self.fund.fund_estimated_percent + ' %)' + '-' + self.fund.fund_estimated_date)
			else:
				split_data = ''
				for i in range(int(self.labs_max_width / 2)):
					split_data += '-'
				self.labs[index].config(text = split_data)
			index += 1

		# Update buttons frames idle tasks to let tkinter calculate buttons sizes
		self.show_frame.update_idletasks()
		self.labs_max_width = 0
		self.lab_max_height = 0
		for lab in self.labs:
			if self.labs_max_width < lab.winfo_width():
				self.labs_max_width = lab.winfo_width()
		if len(self.labs) > max_window_height_line:
			self.lab_max_height = max_window_height_line * self.labs[0].winfo_height()
		else:
			self.lab_max_height = len(self.labs) * self.labs[0].winfo_height()



		# Resize the canvas frame to show
		self.basic_frame.config(width=self.labs_max_width + self.vsb.winfo_width(),
		                    height=self.lab_max_height)
		# self.init = 1
		# print("update")
		# self.fund.get_fund_by_code_num("000001")
		# self.lab1.config(text = self.fund.fund_name + ' : ' + self.fund.fund_estimated_value + ' (' + self.fund.fund_estimated_percent + ' %)')


	def run(self):
		self.win.mainloop()


def update_data():
	global main_ui, update_event
	uptime = 1 # second

	update_event = threading.Event()

	while True:
		main_ui.update_labels()
		# time.sleep(60)
		datedata = handle_date.DateTimeNow()

		if datedata.get_passed_second() > datedata.get_special_passed_second(14,30,0):
			update_event.wait(timeout=default_fast_uptime)
		else:
			update_event.wait(timeout=default_uptime)

		if update_event.isSet():
			break
		# print("1")

def run_ui_window(*window_paras):
	global main_ui, window_update_thread
	print("run_ui_window")
	win = tkinter.Tk()
	main_ui = MainWindow(win, window_paras[0])

	window_update_thread = uithreadControl(1, 'update_window')
	window_update_thread.start()

	# main_ui
	main_ui.run()


class uithreadControl(threading.Thread):
	def __init__(self, threadID, name, *args):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.args = args

	def run(self):
		print ("开始线程：" + self.name)
		if self.name == 'ui_window':
			run_ui_window(self.args[0])
		elif self.name == 'update_window':
			update_data()

	def exit(self):
		global update_event
		update_event.set()

# def Get_Window_Width_Height(code_list):
# 	print("Test")
# 	fund = get_foundation.FoundationData()
# 	stock = get_stock_data_from_sina.SinaStockData()

# 	max_width = 0
# 	max_height = default_char_height
# 	# if len(code_list) > max_window_height_line:
# 	# 	max_height *= max_window_height_line
# 	# else:
# 	# 	max_height *= len(code_list)

# 	for code in code_list:

# 		code_type = code.split(',')[0]
# 		real_code = code.split(',')[1]

# 		if 'stock' == code_type:
# 			stock.get_stock_by_code(real_code)
# 			if max_width < (len(stock.stock_name) + extra_data_len) * default_char_width:
# 				max_width = (len(stock.stock_name) + extra_data_len) * default_char_width
# 		elif 'fund' == code_type:
# 			fund.get_fund_by_code_num(real_code)
# 			if max_width < (len(fund.fund_name) + extra_data_len) * default_char_width:
# 				max_width = (len(fund.fund_name) + extra_data_len) * default_char_width

# 		# print(fund.fund_name)
		
# 			# print(max_width)

# 	return max_width, max_height * len(code_list)



if __name__ == '__main__':    
	print("Testing this module...")
	
	# ui_window_main()

	code_list = ['fund,000001', 'split,split', 'fund,000003', 'fund,000004', 'fund,000005', 'fund,000006', 'fund,000007', 'fund,000008']

	
	thread2 = uithreadControl(2, 'ui_window', code_list)

	# win.mainloop()
	# test.update_labels()
	# test.run()

	
	thread2.start()
	# 
	thread2.join()
	# thread1.join()
