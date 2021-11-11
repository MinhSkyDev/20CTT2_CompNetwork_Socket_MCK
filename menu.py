import subprocess
import socket
import threading
from tkinter import *

root = Tk()
root.title('Main Window')

# Initialize the server
def serverStart():
	cmd = 'python server.py'
	p = subprocess.Popen(cmd, shell = True)
	out, err = p.communicate()
	print(err)
	print(out)
	return

# Initialize the client
def clientStart():
	cmd = 'python client.py'
	p = subprocess.Popen(cmd, shell = True)
	out, err = p.communicate()
	print(err)
	print(out)
	return

# Open the registration window
def registrationWindow():
	registration = Toplevel()
	registration.title('Registration Window')
	return
	

# Creating label widgets
label = Label(root, text = "DO AN MMT - 20CTT2", padx = 50, pady = 50)

# Creating button widgets
serverButton = Button(root, text = "SERVER", padx = 100, pady = 50, command = serverStart)
clientButton = Button(root, text = "CLIENT", padx = 100, pady = 50, command = clientStart)
registerButton = Button(root, text = "REGISTER", padx = 95, pady = 50, command = registrationWindow)

# Placing GUI comps on the root window
label.pack()
serverButton.pack()
clientButton.pack()
registerButton.pack()

root.mainloop()
