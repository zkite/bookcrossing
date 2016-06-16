from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, Length
from bookcrossing.models.models import Book

class BookForm(Form):
    title = StringField('Title', validators=[InputRequired(), Length(max=60)])
    author = StringField('Author', validators=[InputRequired(), Length(max=80)])
    publisher = StringField('Publisher', validators=[InputRequired(), Length(max=40)])

    category_id = SelectField('Category', coerce=int)

    submit = SubmitField('Submit')