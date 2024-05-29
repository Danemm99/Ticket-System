from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired


class EditTicketForm(FlaskForm):
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], validators=[DataRequired()])
    note = TextAreaField('Note', validators=[DataRequired()])
    submit = SubmitField('Update Ticket')


class EditTicketStatusForm(FlaskForm):
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], validators=[DataRequired()])
    submit = SubmitField('Submit')
