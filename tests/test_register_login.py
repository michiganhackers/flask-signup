import unittest
import re
from flask import url_for, current_app
from test_basics import FlaskClientBasicsTestCase, debug_on
from app import db, create_app
from app.models import User

class RegisterLoginTestCase(unittest.TestCase):

	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		self.client = self.app.test_client(use_cookies=True)

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_app_exists(self):
		self.assertFalse(current_app is None)

	def test_app_is_testing(self):
		self.assertTrue(current_app.config['TESTING'])

	def test_home_page(self):
		response = self.client.get(url_for('main.index'))
		self.assertTrue('Sign-up!' in response.data)

	@debug_on()
	def test_register_and_login(self):
		# register new account
		response = self.client.post(url_for('auth.register'), data={
			'email': 'peggy@example.org',
			'username': 'peggy',
			'uniqname': 'peggygoblue',
			'password': 'pass1',
			'password2': 'pass1'
		})
		self.assertTrue(response.status_code == 302)

		# login
		reponse = self.client.post(url_for('auth.login'), data={
			'email': 'peggy@example.org',
			'password': 'pass1'
		}, follow_redirects=True)
		data = response.get_data(as_text=True)
		# self.assertTrue(re.search(b'peggy!', data))
		# self.assertTrue(u'You haven\'t confirmed your account yet.' 
						# in data)

		# confirmation
		user = User.query.filter_by(email='peggy@example.org').first()
		token = user.generate_confirmation_token()
		response = self.client.get(url_for('auth.confirm_email', token=token),
								   follow_redirects=True)
		data = response.get_data(as_text=True)
		self.assertTrue(b"confirmed your email account. Thanks!" in data)

		# change password
		response = self.client.post(url_for('auth.change_password'), data={
			'old_password': 'pass1',
			'password': 'pass2',
			'password2': 'pass2'
		}, follow_redirects=True)
		self.assertTrue(u'Your password has been updated.' in response.data)
		response = self.client.post(url_for('auth.change_password'), data={
			'old_password': 'pass4',
			'password': 'pass3',
			'password2': 'pass3'
		}, follow_redirects=True)
		self.assertTrue(u'Invalid password.' in response.data)

		# log out
		response = self.client.get(url_for('auth.logout'), follow_redirects=True)
		self.assertTrue(u'You have been logged out.' in response.data)

		# password reset request
		response = self.client.post(url_for('auth.password_reset_request'), data={
			'email': 'peggy@example.org'	
		}, follow_redirects=True)
		self.assertTrue(u'An email with instructions to reset your password has been '
			  'sent to you.' in response.data)
		token = user.generate_reset_token()
		response = self.client.post(url_for('auth.password_reset', token=token), data={
			'email': 'peggy@example.org',
			'password': 'pass3',
			'password2': 'pass3'
		}, follow_redirects=True)
		self.assertTrue(u'Your password has been updated.' in response.data)

		# log in
		reponse = self.client.post(url_for('auth.login'), data={
			'email': 'peggy@example.org',
			'password': 'pass3'
		}, follow_redirects=True)
		data = response.get_data(as_text=True)

		# change email request
		response = self.client.post(url_for('auth.change_email_request'), data={
			'email': 'victor@example.org',
			'password': 'pass3'
		}, follow_redirects=True)
		self.assertTrue(u'An email with instructions to confirm your new email '
						'address has been sent to you.' in response.data)
		token = user.generate_email_change_token('victor@example.org')
		response = self.client.get(url_for('auth.change_email', token='random'),
					follow_redirects=True)
		self.assertTrue(u'Invalid request. Perhaps the token has expired.' in response.data)
		response = self.client.get(url_for('auth.change_email', token=token), 
					follow_redirects=True)
		self.assertTrue(u'Your email address has been updated.' in response.data)


