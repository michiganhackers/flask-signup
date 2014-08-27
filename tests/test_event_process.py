import unittest
import re
from flask.ext.login import current_user

from flask import url_for, current_app

from test_basics import FlaskClientBasicsTestCase, debug_on
from app import db, create_app
from app.models import User, Event

class EventTestCase(unittest.TestCase):

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

	@debug_on()
	def test_get_events_list(self):
		response = self.client.get(url_for('events.events_list'))
		data = response.get_data(as_text=True)
		self.assertTrue(u'Events' in data)
		self.assertTrue(response.status_code == 200)

	@debug_on()
	def test_create_event_anonymous_user(self):
		response = self.client.get(url_for('events.create_event'), follow_redirects=True)
		self.assertTrue(response.status_code == 403)

	@debug_on()
	def test_create_event(self):
		u = User(email='peggy@example.com', password='pass1', is_administrator=True)
		db.session.add(u)
		db.session.commit()

		response = self.client.post(url_for('events.create_event'), data= {
			'name': 'event1',
			'code': 'evnt1',
			'date': '07/10/2014 3:58 PM'
		}, follow_redirects=True)
		data = response.get_data(as_text=True)
		self.assertTrue('Your event has been created' in data)

		response = self.client.post(url_for('events.create_event'), data= {
			'name': 'event2',
			'code': 'evnt1',
			'date': '07/10/2014 3:58 PM'
		}, follow_redirects=True)
		data = response.get_data(as_text=True)
		self.assertTrue('That shortcode has already been used' in data)


