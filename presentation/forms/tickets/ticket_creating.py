from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired


class TicketForm(FlaskForm):
    note = TextAreaField('Note', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')])
    group = SelectField('Group', coerce=int)
    submit = SubmitField('Create Ticket')
