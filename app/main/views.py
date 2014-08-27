from flask.ext.login import login_required, current_user

from flask import render_template, current_app

from . import main

@main.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')