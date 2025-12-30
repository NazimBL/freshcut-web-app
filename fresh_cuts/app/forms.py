from flask_wtf import FlaskForm
from wtforms import TimeField, BooleanField, SubmitField
from wtforms.validators import Optional

class AvailabilityForm(FlaskForm):
    start_time = TimeField('Start Time', validators=[Optional()])
    end_time = TimeField('End Time', validators=[Optional()])
    is_closed = BooleanField('Closed?')
    submit = SubmitField('Update')
