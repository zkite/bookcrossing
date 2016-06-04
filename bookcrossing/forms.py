from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class BookFrom(Form):
    id_owner = IntegerField('id_owner', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    category = StringField('category', validators=[DataRequired()])
