from tkinter import *
from DB import *
from tkinter import messagebox
def registrationHandle():
	def submitServer():
		# Create or connect to a database
		conn = sqlite3.connect('loginInfo.db')

		# Create a cursor
		c = conn.cursor()

		# Declare the variables that are gonna get inserted
		usernameResult = username.get()
		passwordResult = password.get()
		checkResult = False

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
		if existServer(usernameResult) == False:
			c.execute("INSERT INTO accountTable VALUES(:username, :password, :clientCheck)",
			{
				  'username': usernameResult,
				  'password': passwordResult,
				  'clientCheck': checkResult
				  })
			conn.commit()
		else:
			messagebox.showerror("Lỗi", "Tài khoản đã tồn tại.")
		# Clear the entries
		username.delete(0, END)
		password.delete(0, END)

		# Close the connection
		conn.close()
	END
	
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
		if existClient(usernameResult) == False:
			c.execute("INSERT INTO accountTable VALUES(:username, :password, :clientCheck)",
			{
				  'username': usernameResult,
				  'password': passwordResult,
				  'clientCheck': checkResult
				  })
			conn.commit()
		else:
			messagebox.showerror("Lỗi", "Tài khoản đã tồn tại.")
		# Clear the entries
		username.delete(0, END)
		password.delete(0, END)

		# Close the connection
		conn.close()
	END

	root = Tk()
	root.title('Đăng ký tài khoản')
	root.geometry("800x450")
	root.resizable(FALSE, FALSE)

	username = Entry(root, width = 30)
	username.grid(row = 0 , column = 1, padx = 20)
	usernameResult = username.get()

	username_label = Label(root, text = "Username")
	username_label.grid(row = 0, column = 0)

	password = Entry(root, width = 30)
	password.grid(row = 1, column = 1, padx = 20)
	passwordResult = password.get()

	password_label = Label(root, text = "Password")
	password_label.grid(row = 1 , column = 0)
	
	

	submitClient_button = Button(root, text = "ĐĂNG KÝ CLIENT", command = submitClient)
	submitClient_button.grid(row = 3, column = 0, rowspan = 1, columnspan = 2, pady = 10, padx = 10, ipadx = 100)

	submitServer_button = Button(root, text = "ĐĂNG KÝ SERVER", command = submitServer)
	submitServer_button.grid(row = 4, column = 0, rowspan = 1, columnspan = 2, pady = 10, padx = 10, ipadx = 100)
