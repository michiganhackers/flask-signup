from flask import render_template, redirect, url_for, flash, request

from . import auth
from .. import db
from .forms import RegistrationForm
from ..models import User
from ..email import send_email


@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)


