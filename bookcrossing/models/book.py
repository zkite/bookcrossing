from bookcrossing import db
from marshmallow_sqlalchemy import ModelSchema

class BookModel(db.Model):
	__tablename__ = 'books'

	id = db.Column('id', db.Integer, primary_key=True)
	title = db.Column('title', db.String(60), nullable=False)
	author = db.Column('author', db.String(80), nullable=False)
	publisher = db.Column('publisher', db.String(40), nullable=False)

	category_id = db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
	user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))

	def __init__(self, title, author, publisher):
		self.title = title
		self.author = author
		self.publisher = publisher

	def __repr__(self):
		return "<Book ID: {0}, Title: {1}, Author: {2}>".format(self.id, self.title, self.author)

#for serializing Book model
class BookSchema(ModelSchema):
	class Meta:
		model = BookModel
