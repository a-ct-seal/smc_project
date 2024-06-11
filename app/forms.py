import sqlalchemy as sa

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, widgets
from wtforms.fields.choices import SelectMultipleField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app import db
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('This username is taken. Please choose a different one.')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class PredictionForm(FlaskForm):
    recommendation = MultiCheckboxField('Recommendation')  # todo add music
    submit = SubmitField('Submit and regen recommendation')
