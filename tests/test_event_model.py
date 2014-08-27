import unittest
import time
from datetime import datetime
from test_basics import BasicsTestCase, debug_on
from app import db
from app.models import User, Event

class EventModelTestCase(BasicsTestCase):

	@debug_on()
	def test_create_event(self):
		e = Event(name='Hack Night', code='hn090814')
		db.session.add(e)
		db.session.commit()
		self.assertTrue(Event.query.filter_by(name='Hack Night').first())

	@debug_on()
	def test_user_event(self):
		e = Event(name='Hack Night', code='hn090814')
		db.session.add(e)
		db.session.commit()
		us = User(email='peggy@example.org')
		us.events.append(e)
		db.session.add(us)
		db.session.commit()
		self.assertTrue(User.query.filter_by(email='peggy@example.org') \
						.first().events.filter_by(name='Hack Night').first())
		self.assertTrue(e.users.filter_by(email='peggy@example.org').first())
		us.events.remove(e)
		db.session.add(us)
		db.session.commit()
		self.assertFalse(User.query.filter_by(email='peggy@example.org') \
						.first().events.filter_by(name='Hack Night').first())
