from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo
from bookcrossing.models.user_model import UserModel


class RegistrationForm(Form):
    login = StringField('Login', validators=[InputRequired('Login is required'),
                                             Length(min=3, max=20,
                                                    message='Username must have from 3 to 12 characters'),
                                             Regexp('^[A-z0-9].*$', message='Use only numbers and letters')],)

    email = StringField('Email', validators=[InputRequired(),
                                             Length(1, 64),
                                             Email()],
                        render_kw={"placeholder": "email@com.com"})

    first_name = StringField('First Name', validators=[InputRequired(),
                                                       Length(min=3, max=256),
                                                       Regexp('^[A-z0-9].*$', message='Use only numbers and letters')])

    last_name = StringField('Last Name', validators=[InputRequired(),
                                                     Length(min=3, max=256),
                                                     Regexp('^[A-z0-9].*$', message='Use only numbers and letters')])

    office = StringField('Office', validators=[InputRequired(),
                                               Length(min=3, max=256),
                                               Regexp('^[A-z0-9].*$', message='Use only numbers and letters')])

    phone_number = StringField('Phone', validators=[InputRequired(),
                                                    Regexp('\d{3}-\d{3}-\d{2}-\d{2}')],
                               render_kw={"placeholder": "example: 063-000-00-00"})

    password = PasswordField('Password', validators=[InputRequired(),
                                                     EqualTo('confirm', message='Passwords must match.')])

    confirm = PasswordField('Confirm password', validators=[InputRequired()])

    submit = SubmitField('Register')

    def validate_email(self, field):
        if UserModel.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_login(self, field):
        if UserModel.query.filter_by(login=field.data).first():
            raise ValidationError('Username already in use.')
