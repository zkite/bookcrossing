from wtforms import Form, StringField
from wtforms.validators import Length, InputRequired

class AddBookForm(Form):
	title = StringField('Title', [InputRequired('Title is required'),
	                              Length(min=6, max=30, message='Title must have from 6 to 30 characters')])
	author = StringField('Author', [InputRequired('Author is required'),
	                              Length(min=6, max=30, message='Author must have from 6 to 30 characters')])
	publisher = StringField('Publisher', [InputRequired('Publisher is required'),
	                              Length(min=6, max=30, message='Publisher must have from 6 to 30 characters')])
	category = StringField('Category', [InputRequired('Category is required'),
	                              Length(min=6, max=30, message='Category must have from 6 to 30 characters')])


class UpdateBookForm(AddBookForm):
	id = StringField('Id')
