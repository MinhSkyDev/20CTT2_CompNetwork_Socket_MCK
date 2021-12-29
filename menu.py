import subprocess
import socket
import threading
import sqlite3
import DB
import traceback
import sys
from registration import registrationHandle
from tkinter import *
from tkinter import messagebox
import os

root = Tk()
root.title('Cửa số chính')
root.geometry("800x450")
root.resizable(FALSE, FALSE)

# Declare global 
global existServerReq
existServerReq = False


# Initialize the server
def serverStart():
	global existServerReq
	# If a server request has not existed yet, proceed
	if existServerReq == False:

		# Change the server request status to True
		existServerReq = True
		cmd = 'python server.py'
		p = subprocess.Popen(cmd, shell = True)
		out, err = p.communicate()

		# Change the server request status to False as the there's no more execution
		existServerReq = False
	else:
		messagebox.showerror('Lỗi', 'Không thể mở nhiều server qua 1 host.')
	return

		


def serverCommand():
	server = threading.Thread(target = serverStart)
	server.start()
	return

# Initialize the client
def clientStart():
	cmd = 'python client.py'
	p = subprocess.Popen(cmd, shell = True)
	out, err = p.communicate()
	return

def clientCommand():
	client = threading.Thread(target = clientStart)
	client.start()


# Open the registration window
def registrationWindow():
	registrationHandle()
	return



img_bg = PhotoImage(file="assest/bg.png")
img_bg_label = Label(root, image = img_bg)
img_bg_label.place(x= 0, y= 0)
# Creating label widgets
##label = Label(root, text = "ĐỒ ÁN MMT - 20CTT2", padx = 50, pady = 50, font=("Verdana", 25))

# Creating button widgets
serverButton = Button(root, text = "SERVER", padx = 20, pady = 20, command = serverCommand, font=("Verdana", 15))
clientButton = Button(root, text = "CLIENT", padx = 20, pady = 20, command = clientCommand, font=("Verdana", 15))
registerButton = Button(root, text = "ĐĂNG KÝ", padx = 20, pady = 20, command = registrationWindow, font=("Verdana", 15))

# Placing GUI comps on the root window
##label.place(relx = 0.5, rely = 0.1, anchor = "center")
serverButton.place(x=474.0,y=122.0,width=272.0,height=77.0)

clientButton.place(x=474.0,y=235.0,width=272.0,height=77.0)

registerButton.place(x=474.0,y=348.0,width=272.0,height=77.0)

root.mainloop()
	
