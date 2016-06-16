from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, EqualTo, InputRequired, Regexp, Email

class RegistrationForm(Form):
	login = StringField('Login', [InputRequired('Login is required'),
	                                    Length(min=5, max=12, message='Username must have from 5 to 12 characters'),
	                                    Regexp('^[A-z0-9].*$', message='Input doesnt match with required pattern')])

	email = StringField('Email', [InputRequired(),
	                              Length(min=7, max=30, message='Email must have from 7 to 30 characters'),
	                              Email(message='Input doesnt match with required pattern')])

	first_name = StringField('First_name', [InputRequired(),
	                                        Length(min=3, max=30, message='First name must have from 3 to 30 characters'),
	                                        Regexp('^[A-z0-9].*$', message='Input doesnt match with required pattern')])

	last_name = StringField('Last_name', [InputRequired(),
                                      Length(min=3, max=30, message='Last name must have from 3 to 30 characters'),
                                      Regexp('^[A-z0-9].*$', message='Input doesnt match with required pattern')])

	office = StringField('Office', [InputRequired(),
                                    Length(min=5, max=30, message='Office must have from 5 to 30 characters'),
                                    Regexp('^[A-z0-9].*$', message='Input doesnt match with required pattern')])

	phone = StringField('Phone', [InputRequired(),
                                  Length(min=6, max=18, message='Phone number must have from 6 to 18 characters'),
                                  Regexp('^[-0-9].*$', message='Input doesnt match with required pattern')])


	password = PasswordField('Password', [InputRequired('Password is required'),
	                                      Length(min=3, max=12, message='Password must have from 3 to 12 characters'),
	                                      EqualTo('confirm', 'Passwords must mutch')])
	
	confirm = PasswordField('Repeat Password')
