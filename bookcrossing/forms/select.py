from wtforms import Form, StringField

class SelectForm(Form):
	select = StringField('Select')