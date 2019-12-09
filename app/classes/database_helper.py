# Import the helper classes
# and the helper libraries 

from flask import Flask
from flask_mysqldb import MySQL 

# This class actually helps
# to create repeated functions 
# which would be used in our dB
# connections via MySQL

class Decagondb:

	# define the function which
	# would aid the cursor object
	# to be created

	def create_connection():

		# the Cursor object holding the
		# connection method

		cur = mysql.connection.cursor()
		return cur

	def execute_query(self, query):

		# return the queries needed
		# to facilitate the funcs

		cur = mysql.connection.cursor()
		execute_func = cur.execute(query)
		return execute_func