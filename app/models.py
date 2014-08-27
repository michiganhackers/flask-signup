from datetime import datetime

from flask import current_app, request, url_for
from . import db



class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True, index=True)
	member_since = db.Column(db.DateTime(), default=datetime.utcnow)

	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
	
	def __repr__(self):
		return '<User email: %r>' % (self.email)

	@staticmethod
	def generate_fake(count=100):
		from sqlalchemy.exc import IntegrityError
		from random import seed
		import forgery_py

		seed()
		for i in range(count):
			u = User(email=forgery_py.internet.email_address(),
					 username=forgery_py.internet.user_name(False),
					 member_since=forgery_py.date.date(True))
			db.session.add(u)
			try:
				db.session.commit()
			except IntegrityError:
				db.session.rollback()
