from wtforms import Form, StringField
from wtforms.validators import Length, InputRequired


class SearchForm(Form):
    search = StringField('BookSearch', [InputRequired(), Length(min=3, max=30)])
    select = StringField('Select')
