#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ui_window

def open_list_file(filename):
	try:
		fp = open(filename, 'r')
		return fp
	except IOError:
		print("%s open failed" %(filename))

if __name__ == '__main__':    
	print("Testing this module...")

	file = open_list_file("fund_codes.txt")

	code_list = []

	while True:
		file_line = file.readline()
		if not file_line:
			break;
		else:
			# Get rid of the end enter char
			file_line = file_line.replace('\n','').replace('\r','')
			code_list.append(file_line)

	file.close()
	# print(code_list)

	win_width, win_height = ui_window.Get_Window_Width_Height(code_list)

	print(win_width)
	print(win_height)

	# thread1= ui_window.uithreadControl(1, 'update_window', 1)
	thread1 = ui_window.uithreadControl(2, 'ui_window', win_width, win_height, code_list)
	# window_update_thread = ui_window.uithreadControl(1, 'update_window')
	
	# win.mainloop()
	# test.update_labels()
	# test.run()

	
	thread1.start()
	# thread2.join()
	
	
	# window_update_thread.start()
	# window_update_thread.join()

	thread1.join()




