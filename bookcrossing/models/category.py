from bookcrossing import db
from marshmallow_sqlalchemy import ModelSchema

class CategoryModel(db.Model):
	__tablename__ = 'categories'

	id = db.Column('id', db.Integer, primary_key=True)
	name = db.Column('name', db.String(20), nullable=False)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return "<Category ID: {0}, Name: {1}>".format(self.id,
		                                              self.name)

#for serializing Category model
class CategorySchema(ModelSchema):
	class Meta:
		model = CategoryModel