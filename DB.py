import sqlite3

# Function to check signup duplicates (CLIENT accounts) 
def existClient(usernameResult):
	# Create or connect to a database
	conn = sqlite3.connect('loginInfo.db')

	# Create a cursor
	c = conn.cursor()

	# Check if the table exists. If it doesn't create one
	c.execute('''SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'accountTable' ''')
	if c.fetchone()[0]== 0: {
		c.execute("""CREATE TABLE accountTable(
		username text,
		password text,
		clientCheck boolean
		)""")
	}

	# Create checkResult for clients' accounts
	checkResult = True

	# Fetch all elements from the database and put them in a list
	c.execute("SELECT * FROM accountTable")
	items = c.fetchall()
	
	# If the list is empty, return as false
	if not items:
		conn.close()
		return False
	# If the list is not empty, check for duplicated usernames and account type (SERVER & CLIENT)
	else:
		for item in items:
			if item[0] == usernameResult and item[2] == checkResult:
				conn.close()
				return True
	conn.close()
	return False

# Function to check signup duplicates (SERVER accounts)
def existServer(usernameResult):
	# Create or connect to a database
	conn = sqlite3.connect('loginInfo.db')

	# Create a cursor
	c = conn.cursor()

	# Check if the table exists. If it doesn't create one
	c.execute('''SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'accountTable' ''')
	if c.fetchone()[0]== 0: {
		c.execute("""CREATE TABLE accountTable(
		username text,
		password text,
		clientCheck boolean
		)""")
	}

	# Create checkResult for servers' accounts
	checkResult = False

	# Fetch all elements from the database and put them in a list
	c.execute("SELECT * FROM accountTable")
	items = c.fetchall()
	
	# If the list is empty, return as false
	if not items:
		conn.close()
		return False
	# If the list is not empty, check for duplicated usernames and account type (SERVER & CLIENT)
	else:
		for item in items:
			if item[0] == usernameResult and item[2] == checkResult:
				conn.close()
				return True

	conn.close()
	return False

# Function to check login validity (CLIENT accounts)
def isValidClient(usernameResult, passwordResult):
	# Create or connect to a database
	conn = sqlite3.connect('loginInfo.db')

	# Create a cursor
	c = conn.cursor()

	# Check if the table exists. If it doesn't create one
	c.execute('''SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'accountTable' ''')
	if c.fetchone()[0]== 0: {
		c.execute("""CREATE TABLE accountTable(
		username text,
		password text,
		clientCheck boolean
		)""")
	}

	# Create checkResult for clients' accounts
	checkResult = True

	# Fetch all elements from the database and put them in a list
	c.execute("SELECT * FROM accountTable")
	items = c.fetchall()
	
	# If the list is empty, return as false
	if not items:
		conn.close()
		return False
	# If the list is not empty, check for validity (username, password, and account type)
	else:
		for item in items:
			if item[0] == usernameResult and item[1] == passwordResult and item[2] == checkResult:
				conn.close()
				return True
	conn.close()
	return False

# Function to check login validity (SERVER accounts)
def isValidServer(usernameResult, passwordResult):
	# Create or connect to a database
	conn = sqlite3.connect('loginInfo.db')

	# Create a cursor
	c = conn.cursor()

	# Check if the table exists. If it doesn't create one
	c.execute('''SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'accountTable' ''')
	if c.fetchone()[0]== 0: {
		c.execute("""CREATE TABLE accountTable(
		username text,
		password text,
		clientCheck boolean
		)""")
	}

	# Create checkResult for servers' accounts
	checkResult = False

	# Fetch all elements from the database and put them in a list
	c.execute("SELECT * FROM accountTable")
	items = c.fetchall()

	# If the list is empty, return as false
	if not items:
		conn.close()
		return False
	# If the list is empty, check for validity (username, password, and account type)
	else:
		for item in items:
			if item[0] == usernameResult and item[1] == passwordResult and item[2] == checkResult:
				conn.close()
				return True
	conn.close()
	return False

