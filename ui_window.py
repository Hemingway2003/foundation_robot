#!/usr/bin/python
# -*- coding: UTF-8 -*-
import threading
import tkinter
import time

import get_foundation

global main_ui, window_update_thread, update_event

default_char_width = 12
default_char_height = 20

default_title = 'Fund List'

default_up_color = 'red'
default_down_color = 'green'

default_uptime = 600 # unit: second

extra_data_len = 30


class MainWindow(object):
	"""docstring for MainWindow"""
	def __init__(self, tk, width, height, codes):
		global window_update_thread, main_ui
		self.init = 0
		# super(MainWindow, self).__init__()
		self.win_width = width
		self.win_height = height
		

		self.win = tk #tkinter.Toplevel(tk)
		self.win.title(default_title)
		self.win.bind('<FocusIn>', self._focus)
		self.win.bind('<FocusOut>', self._unfocus)
		self.win.protocol("WM_DELETE_WINDOW", self._quit)
		# self.win.overrideredirect(True)
		self.win.wm_attributes('-topmost',1)
		self.fund = get_foundation.FoundationData()
		self.fund.get_fund_by_code_num("110013")

		sw = self.win.winfo_screenwidth()
		sh = self.win.winfo_screenheight()

		self.win_x = (sw - width) / 2
		self.win_y = (sh - height) / 2

		self.win.geometry("%dx%d+%d+%d" %(self.win_width, self.win_height, self.win_x, self.win_y))

		canvas = tkinter.Canvas(tk)
		canvas.configure(width = width)
		canvas.configure(height = height)
		canvas.configure(bg = "black")
		canvas.configure(highlightthickness = 0)

		canvas.pack()


		self.codes = []
		self.labs = []
		for code in codes:
			self.codes.append(code)
			lab = tkinter.Label(canvas, fg ='red', bg = 'black', text = 'null' + ' : ' + 'null' + ' (' + 'null' + ' %)' + '-' + 'null')
			lab.pack()
			self.labs.append(lab)



	def _focus(self, event):
		self.win.attributes('-alpha', 1)

	def _unfocus(self, event):
		self.win.attributes('-alpha', 1)

	def _quit(self):
		global window_update_thread
		self.win.destroy()
		window_update_thread.exit()

	def update_labels(self):
		index = 0
		for code in self.codes:
			self.fund.get_fund_by_code_num(code)
			percent = float(self.fund.fund_estimated_percent)
			if percent < 0.0:
				color = default_down_color
			else:
				color = default_up_color

			self.labs[index].config(fg = color, text = self.fund.fund_name + ' : ' + self.fund.fund_estimated_value + ' (' + self.fund.fund_estimated_percent + ' %)' + '-' + self.fund.fund_estimated_date)
			index += 1
		self.init = 1
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
		update_event.wait(timeout=60)
		if update_event.isSet():
			break


		
		# print("1")

def run_ui_window(*window_paras):
	global main_ui, window_update_thread
	print("run_ui_window")
	win = tkinter.Tk()
	main_ui = MainWindow(win, window_paras[0], window_paras[1], window_paras[2])

	window_update_thread = uithreadControl(1, 'update_window')
	window_update_thread.start()

	# main_ui
	main_ui.run()


class uithreadControl(threading.Thread):
	def __init__(self,threadID, name, *args):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.args = args

	def run(self):
		print ("开始线程：" + self.name)
		if self.name == 'ui_window':
			run_ui_window(self.args[0], self.args[1], self.args[2])
		elif self.name == 'update_window':
			update_data()

	def exit(self):
		global update_event
		update_event.set()

def Get_Window_Width_Height(code_list):
	print("Test")
	fund = get_foundation.FoundationData()
	max_width = 0
	max_height = default_char_height

	for code in code_list:
		fund.get_fund_by_code_num(code)
		# print(fund.fund_name)
		if max_width < (len(fund.fund_name) + extra_data_len) * default_char_width:
			max_width = (len(fund.fund_name) + extra_data_len) * default_char_width
			# print(max_width)

	return max_width, max_height * len(code_list)



if __name__ == '__main__':    
	print("Testing this module...")
	
	# ui_window_main()
	code_list = ['000001', '000003']

	
	thread2 = uithreadControl(2, 'ui_window', 500, 100, code_list)

	# win.mainloop()
	# test.update_labels()
	# test.run()

	
	thread2.start()
	# 
	thread2.join()
	# thread1.join()