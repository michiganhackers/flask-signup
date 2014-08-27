from flask.ext.wtf import Form
from wtforms import StringField, DateTimeField, SubmitField
from wtforms.validators import Required, Length
from wtforms import ValidationError

from ..models import User, Event


class CreateEventForm(Form):
    name = StringField('Event Title', validators=[Required(), Length(1, 120)])
    code = StringField('Event Shortcode', validators=[Required(), Length(1, 64)])
    date = DateTimeField('Event Date', validators=[Required()], format='%m/%d/%Y %I:%M %p')
    submit = SubmitField('Create Event')

    def validate_code(self, field):
        if Event.query.filter_by(code=field.data).first():
            raise ValidationError('That shortcode has already been used.')
