from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo
from bookcrossing.models.user_model import UserModel


class RestorePasswordForm(Form):

    login = StringField('Login', validators=[InputRequired(),
                                             Length(min=3, max=256),
                                             Regexp('^[A-z0-9].*$', message='Use only numbers and letters')],
                        render_kw={"placeholder": "enter your registered login"})

    email = StringField('Email', validators=[InputRequired(), Length(1, 64), Email()],
                        render_kw={"placeholder": "enter your registered email"})

    password = PasswordField('New password', validators=[InputRequired(),
                                                         EqualTo('confirm', message='Passwords must match.')])

    confirm = PasswordField('Confirm password', validators=[InputRequired()])

    submit = SubmitField('Send')

    def validate_email(self, field):
        if UserModel.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Wrong Email! Entered your registered email.')
