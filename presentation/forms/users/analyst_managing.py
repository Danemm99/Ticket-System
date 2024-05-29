from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class ManageAnalystForm(FlaskForm):
    analyst = SelectField('Select Analyst', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Assign Analyst')
