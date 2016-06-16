from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp


class LoginForm(Form):
    login = StringField('Login', validators=[InputRequired(), Length(min=3, max=256), Regexp('^[A-z0-9].*$')])

    password = PasswordField('Password', validators=[InputRequired()])

    submit = SubmitField('Login')
