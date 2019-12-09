'''
	import the needed libraries and other
	modules needed for the running of our 
	tests.
'''

from app import app
import unittest

'''
	Initialize the class and then create
	the two methods SetUp and TearDown which
	would aid to create a platform for writing
	our tests
'''

class GoStocksTest(unittest.TestCase):

	'''
		Define the methods for setting up
		the platform for the tests,this 
		method takes the app object as a
		parameter to set the unittest library
	'''

	def setUp(self):
		self.app = app.test_client()
		self.app.testing = True

	def tearDown(self):
		pass

	'''
		Test that the homepage returns
		a status of success on visit
	'''

	def test_homepage_opens_properly(self):
		response = self.app.get('/')
		self.assertEqual(response.status_code, 200) 


	# Test to check that user logins in proerly

	def test_login_page(self):
		data = {'username':'dayo', 'password':'juicewrld999'}
		response = self.app.post('/login', data)
		self.assertEqual(response.status_code, 200)


	# Test that Non auth user cannot see profile
	# user would be redirected to the Login

	def test_non_auth_user_cannot_see_profile(self):
		response = self.app.get('/profile', follow_redirects = True)
		self.assertIn(b'&rsaquo; Login', response.data)


	# Test that wrong login details would get an error 
	# and would also be shown error page

	def test_wrong_login_details_gets_error(self):
		data = {'username': 'mike', 'password': ' '}
		response = self.app.get('/profile', data, follow_redirects = True)
		self.assertEquals(response.status_code, 404)


	# Test that empty login details would get an error 
	# and would also be shown login page

	def test_empty_login_details_gets_error(self):
		data = { }
		response = self.app.post('/login',data, follow_redirects = True)
		self.assertEquals(response.status_code, 200)

	# Test that registered user can purchase stock
	# and would access the page successfully

	def test_auth_user_can_buy_stocks(self):
		data = {'username': 'mike', 'password': 'meow'}
		response = self.app.get('/buystock', data, follow_redirects =True)
		self.assertEquals(response.status_code, 200)
		self.assertIn(b'Buy Stocks', response.data)

	# Test that registered user can fund account
	# and can access the page

	def test_auth_user_can_fund_account(self):
		data = {'username': 'mike', 'password': 'kingdom'}
		response = self.app.post('/fund-account', data, follow_redirects = True)
		self.assertEquals(response.status_code, 200)
		self.assertIn(b'Fund account', response.data)
		self.assertMessageFlashed(' ',  response.data)

	# Test that all users can access the stock
	# Lookup page where the IEX Api is being called

	def test_users_can_view_stock_lookup(self):
		response = self.app.get('/stock-prices', follow_redirects = True)
		self.assertEquals(response.status_code, 200)
		self.assertIn('Buy Stock', response.data) 

	# Test that the Correct details for funding accounts
	# are correctly input by the user else throw error

	def test_correct_details_are_accepted(self):
		data = {'cardno':12398054, 'amount': 230000, 'cvv': 435}
		response = self.app.post('/fund-account', data, follow_redirects = True)
		self.assertEquals(response.status_code, 200)
		self.assertRedirects(302, '/success', message= None)

'''
	The __name__ attribute gives room for
	the current file to be imported as a
	different module into another file
'''

if __name__ == '__main__':
	unittest.main()