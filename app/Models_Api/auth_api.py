'''
	Import the libraries needed for use
	and then clearly import them, make 
	sure that the __init__.py file has
	already been specified.
'''

import jsonify
from flask import Flask 
from flask_mysqldb import MySQL
app   = Flask(__name__)
mysql = MySQL(app)

'''
	This file actually holds the
	API which authenticates the user
	and also create endpoints which 
	would call different user functions.
'''

class GostockApi:

	'''
		Because i'll be creating database connection
		instances in every method i'll just initialize
		it in a variable and call the variable accordingly
	'''

	mysql_connection_obj = mysql.connection.cursor()


'''
	The function below returns the users registered
	on the platform for all, it scans through the 
	users endpoint using a GET method and the data
	is rendered in JSON format
'''

@app.route('/decagonstocks/api/v1/users', methods=["GET"])
def retrieve_all_users():

	# Using MySQL connection and Database
	# call the cursor object and use
	try:
		mysql_connection_obj.execute("SELECT * FROM users")
		retrieve_all = mysql_connection_obj.fetchall()

	'''
		Now that the connection object has returned
		the fetchall property, we then pass the val
		into json format using the jsonify method
	'''


		rows_returned = jsonify(retrieve_all)
		print rows_returned

	'''
		Throw an exception if the connection to
		the Database generated doesn't work and
		if the endpoint doesn't return any data
	'''

	except Exception as e:
		print(str(e))


'''
	The registration enpoint returns the
	values passed in for the user during
	registration and returns a success status
	if successful in Json format
'''

@app.route('/decagonstocks/api/v1/register', methods=["POST", "GET"])
def register_users():
	try:
		if request.method == "POST":
			username = request.form["username"]
			password = request.form["password"]
			email    = request.form["email"]

			
			'''
				The connection object which is created
				is used to query the database to insert
				a user into the database
			'''

			mysql_connection_obj.execute("INSERT INTO users(username, password, email) VALUES(%s, %s, %s)",(username, password,email))
			data = cur.fetchall()

			'''
				Currently the database is not yet
				populated for use,so the data is null
				and therefore the len(data) is 0
			'''

			if len(data) is 0:

				'''
					Throwing return messages in this format
					automatically renders the data in Json
				'''

				return {'statuscode': '200', 'Message': 'User created successfully'}
			else:
				return {'statuscode': '1000', 'Message': str(data[0])}

	except Exception as e:
		print(str(e))

'''
	The function below actually renders the
	endpoint for the user to login and then 
	enable the user's data to be returned via
	json rendered in JSON format.
'''

@app.route('/decagonstocks/api/v1/login', methods=["POST", "GET"])
def login_users():
	try:
		if request.method == "POST":
			username = request.form["username"]
			password = request.form["password"]

			'''
				From the mysql connection object created
				return the data from the database and then
				fetch a single user for use, throw the resp
				in json format using jsonify
			'''

			mysql_connection_obj.execute("SELECT FROM users WHERE username=%s and password=%s", (username, password))
			data = cur.fetchone()

			'''
				Here we want to check if a user's
				data was returned and if not throw
				an error.
			'''

			if data is 0 :
				return {'statuscode':'301', 'Message': 'Not authenticated'}
			else:
				return jsonify(data)

'''
	The function below actually renders the data
	for the external API from iex and its
	related data, it is attributed to all
'''

@app.route('/decagonstocks/api/v1/checkstockquotes', methods=["GET"])
def view_stock_quotes():

	'''
		Remember we are getting our data from an external
		API from the IEX platform and rendering it via views
		so here we would just return the page for the end user
		to view its content ...
	'''

	response = request.get('/stock-prices')
	if response:
		return jsonify(response)
	else:

		# Remember our custom error page handler

		abort(404)


'''
	The function below actually renders the data
	for a particular user who wants to fund acc
	and its related data, it is attributed to a 
	particular user
'''

@app.route('/decagonstocks/api/v1/fundaccount', methods=["POST", "GET"])
def fund_account_api():

	'''
		This particular endpoint is for already logged
		in users and they are required to fund accounts
		using some details/parameters to be passed
	'''

	if request.method == "POST":

		'''
			Return the details and the data from the
			users gotten for funding the account which
			includes the card Numbers and the CVV
		'''

		cardno = request.form["cardno"]
		amount = request.form["amount"]
		cvv    = request.form["cvv"]

		'''
			Create a connection object and then
			query the form values to fit into the
			connection setup
		'''

		mysql_connection_obj.execute("UPDATE users SET cardno=%s, amount=%s, cvv=%s",(cardno, amount, cvv))
		return_details = mysql_connection_obj.fetchone()

		'''
			Check if the data returned is valid and
			matches with already existing data and 
			return true
		'''

		if return_details:
			return jsonify(return_details)
		else:
			return {'statuscode':'401', 'Message':'Not allowed'}

'''
	The function below actually renders the data
	for a particular user who has bought stocks
	and its related data, it is attributed to a 
	particular user
'''

@app.route('/decagonstocks/api/v1/user/1/userstocks', methods=["POST","GET"])
def view_stock():

	'''
		Now return the connection object and then
		return the data for a specific user for the
		stocks the user actually purchased.
	'''

	mysql_connection_obj.execute("SELECT * FROM boughtstocks")

	
	'''
		Here we then select and create the object for
		a particular user and its related data for 
		all, now the fetchdata method pulls the data
	'''

	fetchonestock = mysql_connection_obj.fetchall()

	'''
		Throw the response in the json format
		using the JSONIFY method specified in 
		the Json library
	'''

	return jsonify(fetchonestock)

'''
	The API below is used to retrieve one of the
	stocks a particular user has bought and 
	its corresponding data
'''
@app.route('/decagonstocks/api/v1/user/1/yourstocks/1', methods = ["GET"])
def your_stock():

	'''
		Now return the connection object and then
		return the data for a specific user for the
		stocks the user actually purchased.
	'''

	mysql_connection_obj.execute("SELECT id FROM boughtstocks")

	
	'''
		Here we then select and create the object for
		a particular user and its related data for 
		all, now the fetchdata method pulls the data
	'''

	fetchonestock = mysql_connection_obj.fetchone()

	'''
		Throw the response in the json format
		using the JSONIFY method specified in 
		the Json library
	'''

	return jsonify(fetchonestock)