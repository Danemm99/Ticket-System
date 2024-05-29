from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class EditGroupForm(FlaskForm):
    name = StringField('Group Name', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Update Group')
