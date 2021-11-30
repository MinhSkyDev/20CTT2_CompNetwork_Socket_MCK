import sqlite3

# Function to check signup duplicates (CLIENT accounts) 
def existClient(usernameResult):
	# Create or connect to a database
	conn = sqlite3.connect('loginInfo.db')

	# Create a cursor
	c = conn.cursor()

	# Create checkResult for clients' accounts
	checkResult = TRUE

	# Fetch all elements from the database and put them in a list
	c.execute("SELECT * FROM accountTable")
	items = c.fetchall()
	
	# If the list is empty, return as false
	if not items:
		con.close()
		return FALSE
	# If the list is not empty, check for duplicated usernames and account type (SERVER & CLIENT)
	else:
		for item in items:
			if item[0] == usernameResult and item[2] == checkResult:
				conn.close()
				return TRUE
	conn.close()
	return FALSE

# Function to check signup duplicates (SERVER accounts)
def existServer(usernameResult):
	# Create or connect to a database
	conn = sqlite3.connect('loginInfo.db')

	# Create a cursor
	c = conn.cursor()

	# Create checkResult for servers' accounts
	checkResult = FALSE

	# Fetch all elements from the database and put them in a list
	c.execute("SELECT * FROM accountTable")
	items = c.fetchall()
	
	# If the list is empty, return as false
	if not items:
		conn.close()
		return FALSE
	# If the list is not empty, check for duplicated usernames and account type (SERVER & CLIENT)
	else:
		for item in items:
			if item[0] == usernameResult and item[2] == checkResult:
				conn.close()
				return TRUE

	conn.close()
	return FALSE

# Function to check login validity (CLIENT accounts)
def isValidClient(usernameResult, passwordResult):
	# Create or connect to a database
	conn = sqlite3.connect('loginInfo.db')

	# Create a cursor
	c = conn.cursor()

	# Create checkResult for clients' accounts
	checkResult = TRUE

	# Fetch all elements from the database and put them in a list
	c.execute("SELECT * FROM accountTable")
	items = c.fetchall()
	
	# If the list is empty, return as false
	if not items:
		conn.close()
		return FALSE
	# If the list is not empty, check for validity (username, password, and account type)
	else:
		for item in items:
			if item[0] == usernameResult and item[1] == passwordResult and item[2] == checkResult:
				conn.close()
				return TRUE
	conn.close()
	return FALSE

# Function to check login validity (SERVER accounts)
def isValidServer(usernameResult, passwordResult):
	# Create or connect to a database
	conn = sqlite3.connect('loginInfo.db')

	# Create a cursor
	c = conn.cursor()

	# Create checkResult for servers' accounts
	checkResult = FALSE

	# Fetch all elements from the database and put them in a list
	c.execute("SELECT * FROM accountTable")
	items = c.fetchall()

	# If the list is empty, return as false
	if not items:
		conn.close()
		return FALSE
	# If the list is empty, check for validity (username, password, and account type)
	else:
		for item in items:
			if item[0] == usernameResult and item[1] == passwordResult and item[2] == checkResult:
				conn.close()
				return TRUE
	conn.close()
	return FALSE

