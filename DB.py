import sqlite3
from tkinter import *
from tkinter import messagebox

def checkUserExist(usernameResult, passwordResult, checkResult):
	# Create or connect to a database
	conn = sqlite3.connect('loginInfo.db')

	# Create a cursor
	c = conn.cursor()

	# Fetch all elements from the database and put them in a list
	c.execute("SELECT * FROM accountTable")
	items = c.fetchall()
	
	# If the list is empty, commit the changes
	if not items:
		return FALSE
	# If the list is not empty, check for duplicated usernames and account type (SERVER & CLIENT)
	else:
		for item in items:
			if item[0] == usernameResult and item[2] == checkResult:
				messagebox.showerror(title = "LỖI", message = "Tài khoản đã tồn tại.")
				return TRUE
			else:
				return FALSE

def submitClient():
	# Create or connect to a database
	conn = sqlite3.connect('loginInfo.db')

	# Create a cursor
	c = conn.cursor()

	# Declare the variables that are gonna get inserted
	usernameResult = username.get()
	passwordResult = password.get()
	checkResult = TRUE

	# Check if the table exists. If it doesn't create one
	c.execute('''SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'accountTable' ''')
	if c.fetchone()[0]== 0: {
		c.execute("""CREATE TABLE accountTable(
		username text,
		password text,
		clientCheck boolean
		)""")
	}

	# If the user doesn't exist in the database, commit the changes
	if checkUserExist(usernameResult, passwordResult, checkResult) == FALSE:
		c.execute("INSERT INTO accountTable VALUES(:username, :password, :clientCheck)",
		{
			  'username': usernameResult,
			  'password': passwordResult,
			  'clientCheck': checkResult
			  })
		conn.commit()
	
	# Clear the entries
	username.delete(0, END)
	password.delete(0, END)

	# Close the connection
	conn.close()

def submitServer():
	# Create or connect to a database
	conn = sqlite3.connect('loginInfo.db')

	# Create a cursor
	c = conn.cursor()

	# Declare the variables that are gonna get inserted
	usernameResult = username.get()
	passwordResult = password.get()
	checkResult = FALSE

	# Check if the table exists. If it doesn't create one
	c.execute('''SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'accountTable' ''')
	if c.fetchone()[0]== 0: {
		c.execute("""CREATE TABLE accountTable(
		username text,
		password text,
		clientCheck boolean
		)""")
	}

	# If the user doesn't exist in the database, commit the changes
	if checkUserExist(usernameResult, passwordResult, checkResult) == FALSE:
		c.execute("INSERT INTO accountTable VALUES(:username, :password, :clientCheck)",
		{
			  'username': usernameResult,
			  'password': passwordResult,
			  'clientCheck': checkResult
			  })
		conn.commit()
	
	# Clear the entries
	username.delete(0, END)
	password.delete(0, END)

	# Close the connection
	conn.close()

def registrationHandle():
	registration = Toplevel()
	registration.title('Đăng ký tài khoản')
	username = Entry(registration, width = 30)
	username.grid(row = 0 , column = 1, padx = 20)
	usernameResult = username.get()
	password = Entry(registration, width = 30)
	password.grid(row = 1, column = 1, padx = 20)
	passwordResult = password.get()
	username_label = Label(registration, text = "Username")
	username_label.grid(row = 0, column = 0)

	password_label = Label(registration, text = "Password")
	password_label.grid(row = 1 , column = 0)

	submitClient_button = Button(registration, text = "ĐĂNG KÝ", command = submitClient)
	submitClient_button.grid(row = 3, column = 0, rowspan = 2, columnspan = 2, pady = 10, padx = 10, ipadx = 100)