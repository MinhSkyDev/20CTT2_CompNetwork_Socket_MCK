import subprocess
import socket
import threading
import sqlite3
import DB
from tkinter import *

from DB import registrationHandle

root = Tk()
root.title('Cửa sổ chính')
root.geometry("800x450")
root.resizable(FALSE, FALSE)

# Initialize the server
def serverStart():
	cmd = 'python server.py'
	p = subprocess.Popen(cmd, shell = True)
	out, err = p.communicate()
	print(err)
	print(out)
	return

def serverCommand():
	server = threading.Thread(target = serverStart)
	server.start()

# Initialize the client
def clientStart():
	cmd = 'python client.py'
	p = subprocess.Popen(cmd, shell = True)
	out, err = p.communicate()
	print(err)
	print(out)
	return

def clientCommand():
	client = threading.Thread(target = clientStart)
	client.start()


# Open the registration window
def registrationWindow():
	registrationHandle()
	return




# Creating label widgets
label = Label(root, text = "ĐỒ ÁN MMT - 20CTT2", padx = 50, pady = 50, font=("Verdana", 25))

# Creating button widgets
serverButton = Button(root, text = "ĐĂNG NHẬP SERVER", padx = 50, pady = 50, command = serverCommand, font=("Verdana", 15))
clientButton = Button(root, text = "ĐĂNG NHẬP CLIENT", padx = 50, pady = 50, command = clientCommand, font=("Verdana", 15))
registerButton = Button(root, text = "ĐĂNG KÝ", padx = 200, pady = 50, command = registrationWindow, font=("Verdana", 15))

# Placing GUI comps on the root window
label.place(relx = 0.5, rely = 0.1, anchor = "center")
serverButton.place(relx = 0.25, rely = 0.4, anchor = "center")
clientButton.place(relx = 0.75, rely = 0.4, anchor = "center")
registerButton.place(relx = 0.5, rely = 0.8, anchor = "center")
root.mainloop()
