# Import the Flask libraries 
# used for powering the Main Event loop

try:
	from flask import Flask
	from flask import flash
	from flask import url_for
	from flask import redirect
	from flask import request
	from flask import session
	from flask import make_response
	from hashlib import md5
	from flask import render_template
	from flask_mysqldb import MySQL
	from flask import jsonify
	import requests
	import json

# Throw an exception Handler that
# Throws an ImportError exception

except ImportError as err:

	# Print to the EndUser a Modified
	# Error Notice to show clear descriptions
	print ("The Module could not be Imported {}". format(err))

# Initialize the Database connection
# and specific environmental variables
# and application configuration vars

app = Flask(__name__)
app.secret_key = "SECRET_KEY"

# Start for the Database Configurations
# Am Implementing MySQL for the database

app.config["MYSQL_DB"]		 = "stocks"
app.config["MYSQL_HOST"]     = "Localhost"
app.config["MYSQL_USER"] 	 = "root"
app.config["MYSQL_PASSWORD"] = ""

# Create a Model representing the 
# Database to create different Objects
mysql = MySQL(app)


# We need a custom error handler
# to throw custom errors that would
# be user friendly to the eyes
@app.errorhandler(404)
def not_found(error):
	return jsonify({'error':'Not found'}),404


# Create the route decorators for 
# handling different functions via
# the Main application.
@app.route('/')
def homepage():

	# Check if user  is logged in
	if 'loggedin' in session:
		return render_template('home.html', username=session['username'])

	# Return the templating view
	return render_template('home.html')



# This function returns all the users
# Registered on the Platform
@app.route('/users')
def users():

	# initiate a database connection
	cur = mysql.connection.cursor()

	# return all users using the Execute
	# function via generated Cursor
	cur.execute("SELECT * FROM users")

	# Fetch all the data needed using
	# the Cursor fetch function
	fetch_data = cur.fetchall()

	# return the templating view
	# with the corresponding data
	return render_template('user.html', data = fetch_data)



# This function actually powers the registration
# of new users and inserts them via database
@app.route('/register', methods = ["POST", "GET"])
def register():

	# Check if there is a POST request
	# and return true for the values 
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		email_ad = request.form["email"]

		# Now create a connection and insert
		# data into the database generally
		cur = mysql.connection.cursor()

		# Execute the insert statement, using Prepared
		# statements to avoid MySQL Injections.
		cur.execute("INSERT INTO users(username, password, email) VALUES(%s, %s, %s)", (username, password, email_ad))

		# Commit the changes into the database
		mysql.connection.commit()
		return redirect(url_for('login'))
	return render_template('register.html')



# This function would help us to update
# Our data in event of viewing it 
@app.route('/update', methods = ["POST", "GET"])
def update():

	# Check if the details are already on
	# and then update the data as supposed
	if request.method == "POST":
		id_data  = request.form["id"] 		
		email = request.form["email"]
		username = request.form["username"]
		password = request.form["password"]

		# Create a cursor and create a
		# connection that would power it
		cur = mysql.connection.cursor()

		# Execute the update details too
		# and populate the database
		cur.execute("UPDATE users SET username=%s, password=%s, email=%s WHERE id=%s",(username, password, email, id_data))

		# Commit the changes to the database
		mysql.connection.commit()
		return redirect(url_for('users'))
	# return render_template('user.html')



# This function would help us to delete
# Our data in event of the activity loop
@app.route('/delete/<string:id_data>', methods = ["POST","GET"])
def delete(id_data):

	# Create a connnection that would help
	# initialize a delete func helper.
	cur = mysql.connection.cursor()

	# Execute the delete Function to remove
	# a user detail ASAP
	cur.execute("DELETE FROM users WHERE id=%s", (id_data))

	# Commit the change and return a 
	# Flash Message of success
	mysql.connection.commit()
	return redirect(url_for('users'))



# This function helps us in creating an individual
# Editing field for a particular user
@app.route('/edituser/<string:id_data>', methods=["GET"])
def edit(id_data):

	# Create the connection that would 
	# power the Editing function
	cur = mysql.connection.cursor()

	# Execute the Editing function to aid in 
	# fixing the edit variables gotten from
	# the forms in general.
	cur.execute("SELECT * FROM users WHERE id=%s", (id_data))
	fetchuser = cur.fetchone()
	return render_template('edit.html', data = fetchuser)



# The login function that takes one id
# and returns associated data
@app.route('/login', methods=["POST", "GET"])
def login():
	
	# Output message if something goes wrong...
    msg = ''

    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))

        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:

            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]

            # Redirect to home page
            return redirect(url_for('profile'))
        else:

            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)



# Function for the user profile after
# Login with required details
@app.route('/profile')
def profile():

    # Check if user is loggedin
    if 'loggedin' in session:

        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', [session['id']])
        account = cursor.fetchone()

        # Show the profile page with account info
        return render_template('profile.html', account=account)

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



# Function for already logged
# in user to logout
@app.route('/logout')
def logout():

	# Remove session data, this will log the user out
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)

	# Redirect to login page
	return redirect(url_for('login'))



## Callback success page for user
## after payment Notifications
@app.route('/success')
def success():

	# return a success page thanking user for 
	# funding his/her account
	try:
		return render_template('success.html')
	except Exception, e:
		return(str(e))



# The route below takes us to the 
# IEX api page where end-users can see iex 
# prices and related companies
# API call here
@app.route('/stock-prices')
def iex():
	re = requests.get('https://cloud.iexapis.com/v1/stock/market/batch?&types=quote&symbols=aapl,fb,googl,tsla,ba,baba&token=sk_61cb076ca68543428e7b04ee40f3c574')
	data = re.json()
	return render_template('quotes.html', quote = data)


# This function actually powers the funding
# of accounts and inserts them via database
@app.route('/fund-account', methods = ["POST", "GET"])
def fundaccount():

	# Check if there is a POST request
	# and return true for the values 
	if request.method == "POST":
		username = session['username']
		cardno   = request.form["cardno"]
		amount   = request.form["amount"]
		cvv      = request.form["cvv"]

		# Now create a connection and insert
		# data into the database generally
		cur = mysql.connection.cursor()

		# Execute the insert statement, using Prepared
		# statements to avoid MySQL Injections.
		cur.execute("UPDATE users SET cardno=%s, amount=%s, cvv=%s WHERE username=%s", (cardno, amount, cvv,username))

		# Commit the changes into the database
		mysql.connection.commit()
		return redirect(url_for('success'))
	return render_template('fund.html')


# Buy Stocks Page for user
@app.route('/buystock')
def buystock():
	re = requests.get('https://cloud.iexapis.com/v1/stock/market/batch?&types=quote&symbols=aapl,fb,googl,tsla,ba,baba&token=sk_61cb076ca68543428e7b04ee40f3c574')
	data = re.json()
	return render_template('buystock.html', quote = data)



# This function actually powers the funding
# of accounts and inserts them via database
@app.route('/completedstock', methods = ["POST", "GET"])
def completedstock():

	# Check if there is a POST request
	# and return true for the values 
	if request.method == "POST":
		username = session['username']
		symbol   = request.form["symbol"]
		amount   = request.form["amount"]

		# Now create a connection and insert
		# data into the database generally
		cur = mysql.connection.cursor()

		# Execute the insert statement, using Prepared
		# statements to avoid MySQL Injections.
		cur.execute("INSERT INTO boughtstocks(symbol, amount, user) VALUES(%s, %s, %s)",(symbol, amount,username))

		# Commit the changes into the database
		mysql.connection.commit()
		return redirect(url_for('yourstock'))
	return render_template('fund.html')


# Get all the stocks Bought by 
# A single user and return vals
@app.route('/yourstock')
def yourstock():

	# create and initialize a connection
	cur  = mysql.connection.cursor()

	# Execute and run the query to get vals
	cur.execute("SELECT * FROM boughtstocks WHERE user=%s",[session['username']])

	# Fetch the data for just one person
	fetchonestock = cur.fetchall()

	# return the template and pass
	# the data to the views

	return render_template('yourstocks.html', data=fetchonestock)

'''
	The __name__ attribute gives room for
	the current file to be imported as a
	different module into another file
'''

if __name__ == '__main__':
	app.run(debug=True)
