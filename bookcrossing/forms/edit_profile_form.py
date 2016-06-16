from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp

class EditProfileForm(Form):

    first_name = StringField('First Name', validators=[InputRequired(), Length(min=3, max=256), Regexp('^[A-z0-9].*$')])

    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=3, max=256), Regexp('^[A-z0-9].*$')])

    office = StringField('Office', validators=[InputRequired(), Length(min=3, max=256), Regexp('^[A-z0-9].*$')])

    phone_number = StringField('Phone Number',
                               validators=[InputRequired(), Length(min=3, max=256), Regexp('^[A-z0-9].*$')])

    submit = SubmitField('Update')
