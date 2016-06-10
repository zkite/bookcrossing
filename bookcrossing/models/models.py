import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column('id', db.Integer, primary_key=True, unique=True, autoincrement=True)
	login = db.Column('login', db.String(30), nullable=False, unique=True)
	password = db.Column('password', db.String(30), nullable=False)
	email = db.Column('email', db.String(60), nullable=False, unique=True)
	first_name = db.Column('first_name', db.String(30))
	last_name = db.Column('last_name', db.String(30))
	office = db.Column('office', db.String(20))  #, nullable=False)
	phone_number = db.Column('phone_number', db.String(20))
	limit = db.Column('limit', db.Integer, default=0)
	points = db.Column('points', db.Integer, default=0)

	office_id = db.Column('office_id', db.Integer, db.ForeignKey('offices.id'))

	def __init__(self, login, password, email, first_name, last_name, office, phone_number):
		self.login = login
		self.password = password
		self.email = email
		self.first_name = first_name
		self.last_name = last_name
		self.office = office.name
		self.phone_number = phone_number

	def __repr__(self):
		return "<User ID: {0}, Login: {1}, Office: {2}, Email: {3}>".format(self.id,
		                                                                     self.login,
		                                                                     self.office,
		                                                                     self.email)


class Office(db.Model):
	__tablename__ = 'offices'

	id = db.Column('id', db.Integer, primary_key=True)
	name = db.Column('name', db.String(20), nullable=False)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return "<Office ID: {0}, Name: {1}>".format(self.id,
		                                            self.name)


class Category(db.Model):
	__tablename__ = 'categories'

	id = db.Column('id', db.Integer, primary_key=True)
	name = db.Column('name', db.String(20), nullable=False)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return "<Category ID: {0}, Name: {1}>".format(self.id,
		                                              self.name)


class Book(db.Model):
	__tablename__ = 'books'

	id = db.Column('id', db.Integer, primary_key=True)
	title = db.Column('title', db.String(60), nullable=False)
	author = db.Column('author', db.String(80), nullable=False)
	publisher = db.Column('publisher', db.String(40), nullable=False)

	category_id = db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
	user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))

	def __init__(self, title, author, publisher, category):
		self.title = title
		self.author = author
		self.publisher = publisher
		self.category = category.name


	def __repr__(self):
		return "<Book ID: {0}, Title: {1}, Author: {2}, Category: {3}>".format(self.id,
		                                                                       self.title,
		                                                                       self.author,
		                                                                       self.category)


class BookRequest(db.Model):
	__tablename__ = 'requests'

	id = db.Column('id', db.Integer, primary_key=True)
	request_date = db.Column('request_date', db.DateTime, nullable=False)
	accept_date = db.Column('accept_date', db.DateTime)
	notification_counter = db.Column('notification_counter', db.Integer, default=0)

	book_id = db.Column('book_id', db.Integer, db.ForeignKey('books.id'))
	req_user_id = db.Column('req_user_id', db.Integer, db.ForeignKey('users.id'))
	owner_user_id = db.Column('owner_user_id', db.Integer, db.ForeignKey('users.id'))

	def __init__(self, request_date=datetime.utcnow(), accept_date=None):
		self.request_date = request_date
		self.accept_date = accept_date

	def __repr__(self):
		return "<Request ID: {0}, REQ_DATE: {1}, ACPT_DATE: {2}, BOOK: {3}, USER: {4}, OWNER: {5}>".format(self.id,
		                                                                                                   self.request_date,
		                                                                                                   self.accept_date,
		                                                                                                   self.book_id,
		                                                                                                   self.req_user_id,
		                                                                                                   self.owner_user_id)