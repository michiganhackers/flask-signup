from flask.ext.login import login_required, current_user

from flask import render_template, redirect, url_for, flash, current_app, request

from .forms import CreateEventForm
from . import events
from .. import db
from ..models import User, Event
from ..decorators import admin_required

@events.route('/', methods=['GET', 'POST'])
def events_list():
	page = request.args.get('page', 1, type=int)
	pagination = Event.query.order_by(Event.date.desc()).paginate(
		page, per_page=10,
		error_out=False)
	events = pagination.items
	return render_template('events/events_list.html', events=events, pagination=pagination)

@events.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_event():
	form = CreateEventForm()
	if form.validate_on_submit():
		event = Event(name=form.name.data,
					  code=form.code.data,
					  date=form.date.data)
		db.session.add(event)
		db.session.commit()
		flash('Your event has been created. Have users text %s to attend.' % event.code)
		return redirect(url_for('main.index'))
	return render_template('events/create.html', form=form)

@events.route('/register', methods=['GET', 'POST'])
def register():
	import twilio.twiml
	resp = twilio.twiml.Response()
	resp.message("Hello, Mobile Monkey")
	return str(resp)

