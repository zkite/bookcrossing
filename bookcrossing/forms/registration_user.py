from flask_wtf import Form
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo
from bookcrossing.models.models import User


class RegistrationForm(Form):
    login = StringField('Login', validators=[InputRequired(), Length(min=3, max=256), Regexp('^[A-z0-9].*$')])

    email = StringField('Email', validators=[InputRequired(), Length(1, 64), Email()])

    first_name = StringField('First Name', validators=[InputRequired(), Length(min=3, max=256), Regexp('^[A-z0-9].*$')])

    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=3, max=256), Regexp('^[A-z0-9].*$')])

    office = StringField('Office', validators=[InputRequired(), Length(min=3, max=256), Regexp('^[A-z0-9].*$')])

    phone_number = StringField('Phone Number',
                               validators=[InputRequired(), Length(min=3, max=256), Regexp('^[A-z0-9].*$')])

    password = PasswordField('Password',
                             validators=[InputRequired(), EqualTo('password2', message='Passwords NOT match.')])

    password2 = PasswordField('Confirm password', validators=[InputRequired()])

    submit = SubmitField('Register')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user and user.id != current_user.id:
            raise ValidationError('Email already registered.')

    def validate_login(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user and user.id != current_user.id:
            raise ValidationError('Username already in use.')


class LoginForm(Form):
    login = StringField('Login', validators=[InputRequired(), Length(min=3, max=256), Regexp('^[A-z0-9].*$')])

    password = PasswordField('Password', validators=[InputRequired()])

    submit = SubmitField('LogIn')
