import unittest
import time
from datetime import datetime
from test_basics import BasicsTestCase
from app import db
from app.models import User, AnonymousUser

class UserModelTestCase(BasicsTestCase):
	def test_password_setter(self):
		u = User(password='pass1')
		self.assertTrue(u.password_hash is not None)

	def test_no_password_getter(self):
		u = User(password='pass1')
		with self.assertRaises(AttributeError):
			u.password

	def test_password_verification(self):
		u = User(password='pass1')
		self.assertTrue(u.verify_password(password='pass1'))
		self.assertFalse(u.verify_password(password='pass2'))

	def test_password_salts_are_random(self):
		u = User(password='pass')
		u2 = User(password='pass')
		self.assertTrue(u.password_hash != u2.password_hash)

	def test_valid_confirmation_token(self):
		u = User(password='pass1')
		db.session.add(u)
		db.session.commit()
		token = u.generate_confirmation_token()
		self.assertTrue(u.confirm_email(token))

	def test_invalid_confirmation_token(self):
		u1 = User(password='pass1')
		u2 = User(password='pass2')
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		token = u1.generate_confirmation_token()
		self.assertFalse(u2.confirm_email(token))

	def test_expired_confirmation_token(self):
		u = User(password='pass1')
		db.session.add(u)
		db.session.commit()
		token = u.generate_confirmation_token(1)
		time.sleep(2)
		self.assertFalse(u.confirm_email(token))

	def test_valid_reset_token(self):
		u = User(password='pass1')
		db.session.add(u)
		db.session.commit()
		token = u.generate_reset_token()
		self.assertTrue(u.reset_password(token, 'pass2'))
		self.assertTrue(u.verify_password('pass2'))

	def test_invalid_reset_token(self):
		u1 = User(password='pass1')
		u2 = User(password='pass2')
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		token = u1.generate_reset_token()
		self.assertFalse(u2.reset_password(token, 'pass3'))
		self.assertTrue(u2.verify_password('pass2'))

	def test_valid_email_change_token(self):
		u = User(email='peggy@example.com', password='pass1')
		db.session.add(u)
		db.session.commit()
		token = u.generate_email_change_token('victor@example.org')
		self.assertTrue(u.change_email(token))
		self.assertTrue(u.email == 'victor@example.org')

	def test_invalid_email_change_token(self):
		u1 = User(email='peggy@example.com', password='pass1')
		u2 = User(email='victor@example.org', password='pass2')
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		token = u1.generate_email_change_token('bob@example.net')
		self.assertFalse(u2.change_email(token))
		self.assertTrue(u2.email == 'victor@example.org')

	def test_duplicate_email_change_token(self):
		u1 = User(email='peggy@example.com', password='pass1')
		u2 = User(email='victor@example.org', password='pass2')
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		token = u2.generate_email_change_token('peggy@example.com')
		self.assertFalse(u2.change_email(token))
		self.assertTrue(u2.email == 'victor@example.org')

	def test_is_administrator(self):
		u = User(email='peggy@example.com', password='pass1', is_administrator=True)
		db.session.add(u)
		db.session.commit()
		self.assertTrue(u.is_administrator)

	def test_is_not_administrator(self):
		u = User(email='peggy@example.com', password='pass1', is_administrator=False)
		db.session.add(u)
		db.session.commit()
		self.assertFalse(u.is_administrator)

	def test_anonymous_user(self):
		u = AnonymousUser()
		self.assertFalse(u.is_administrator())

	def test_timestamps(self):
		u = User(password='pass1')
		db.session.add(u)
		db.session.commit()
		self.assertTrue((datetime.utcnow() - u.member_since).total_seconds() < 3)
		self.assertTrue((datetime.utcnow() - u.last_seen).total_seconds() < 3)

	def test_ping(self):
		u = User(password='pass1')
		db.session.add(u)
		db.session.commit()
		time.sleep(2)
		last_seen_before = u.last_seen
		u.ping()
		self.assertTrue(u.last_seen > last_seen_before)


