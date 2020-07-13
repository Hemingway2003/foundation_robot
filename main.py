#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ui_window

def open_list_file(filename):
	try:
		fp = open(filename, 'r')
		return fp
	except IOError:
		print("%s open failed" %(filename))

def get_file_lines(file_name, list, type):
	file = open_list_file(file_name)

	if file:
		while True:
			file_line = file.readline()
			if not file_line:
				break;
			else:
				if '#' == file_line[0:1]:
					continue
				else:
					# Get rid of the end enter char
					file_line = file_line.replace('\n','').replace('\r','')
					list.append(type + ',' + file_line)
		file.close()

		if 'stock' == type:
			list.append('split' + ',' + 'split')

if __name__ == '__main__':    
	print("Testing this module...")


	code_list = []

	get_file_lines('stock_codes.txt', code_list, 'stock')

	get_file_lines('fund_codes.txt', code_list, 'fund')

	# print(code_list)
	

	win_width, win_height = ui_window.Get_Window_Width_Height(code_list)

	print(win_width)
	print(win_height)

	thread1 = ui_window.uithreadControl(2, 'ui_window', win_width, win_height, code_list)


	
	thread1.start()

	thread1.join()




