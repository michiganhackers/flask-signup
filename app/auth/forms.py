from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

from ..models import User


class RegistrationForm(Form):
	email = StringField('Email', validators=[Required(), Length(1, 64),
											 Email()])
	submit = SubmitField('Sign up')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')



