from flask_login import UserMixin
from bookcrossing import db
from marshmallow_sqlalchemy import ModelSchema


class UserModel(UserMixin, db.Model):
	__tablename__ = 'users'

	id = db.Column('id', db.Integer, primary_key=True, unique=True, autoincrement=True)
	login = db.Column('login', db.String(30), nullable=False, unique=True)
	password = db.Column('password', db.String(100), nullable=False)
	email = db.Column('email', db.String(60), nullable=False, unique=True)
	first_name = db.Column('first_name', db.String(30))
	last_name = db.Column('last_name', db.String(30))
	office = db.Column('office', db.String(20), nullable=False)
	phone_number = db.Column('phone_number', db.String(20))

	limit = db.Column('limit', db.Integer, default=0)
	points = db.Column('points', db.Integer, default=0)

	# office_id = db.Column('office_id', db.Integer, db.ForeignKey('offices.id'))

	def __init__(self, login, password, email, first_name, last_name, office, phone_number):
		self.login = login
		self.password = password
		self.email = email
		self.first_name = first_name
		self.last_name = last_name
		self.office = office
		# self.office = office.name
		self.phone_number = phone_number

	def is_owner(self, book_user_id):
		return self.id == book_user_id

	def __repr__(self):
		return "<User ID: {0}, Login: {1}, Office: {2}, Email: {3}, Password: {4}>".format(self.id,
	                                                                                       self.login,
	                                                                                       self.office,
	                                                                                       self.email,
	                                                                                       self.password)