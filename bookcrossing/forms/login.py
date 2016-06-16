from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, InputRequired, Regexp


class LoginForm(Form):
    login = StringField('Login', [InputRequired('Login is required'),
                                  Length(min=5, max=12, message='Username must have from 5 to 12 characters'),
                                  Regexp('^[A-z0-9].*$', message='Input doesnt match with required pattern')])

    password = PasswordField('Password', [InputRequired('Password is required'),
                                          Length(min=3, max=12, message='Password must have from 3 to 12 characters')])
