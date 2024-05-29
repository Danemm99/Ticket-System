from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, ValidationError
from presentation.models.user import User


class AddManagerForm(FlaskForm):
    email = StringField('Manager Email', validators=[DataRequired(), Email()])
    group_id = SelectField('Select Group', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Manager')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('No user with this email found.')
        if user.role != 'manager':
            raise ValidationError('User is not a manager.')
        if user.group_id is not None:
            raise ValidationError('User already has a group.')
