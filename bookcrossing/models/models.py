import datetime

from bookcrossing.models import (db,
                                 login_manager)

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True, unique=True, autoincrement=True)
    login = db.Column('login', db.String(30), nullable=False, unique=True)
    password_hash = db.Column('password_hash', db.String(100), nullable=False)
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

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User ID: {0}, Login: {1}, Office: {2}, Email: {3}, Password: {4}>".format(self.id,
                                                                                           self.login,
                                                                                           self.office,
                                                                                           self.email,
                                                                                           self.password_hash)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Office(db.Model):
    __tablename__ = 'offices'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(20), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Office: {0}>".format(self.name)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(20), nullable=False)

    books = db.relationship('Book', backref='category')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Category: {0}>".format(self.name)


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(60), nullable=False)
    author = db.Column('author', db.String(80), nullable=False)
    publisher = db.Column('publisher', db.String(40), nullable=False)
    visible = db.Column('visible', db.Boolean, default=True)
    category_id = db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, author, publisher, category):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.category = category

    def __repr__(self):
        return "<Book Title: {0}, Author: {1}, Category: {2}>".format(self.title,
                                                                      self.author,
                                                                      self.category)


class BookRequest(db.Model):
    __tablename__ = 'requests'

    id = db.Column('id', db.Integer, primary_key=True)
    request_date = db.Column('request_date', db.DateTime, nullable=False)
    accept_date = db.Column('accept_date', db.DateTime, default=None)
    notification_counter = db.Column('notification_counter', db.Integer, default=0)
    book_id = db.Column('book_id', db.Integer, db.ForeignKey('books.id'))
    req_user_id = db.Column('req_user_id', db.Integer, db.ForeignKey('users.id'))
    owner_user_id = db.Column('owner_user_id', db.Integer, db.ForeignKey('users.id'))

    def __init__(self, book_id, req_user_id, owner_user_id,
                 request_date=datetime.datetime.utcnow()):
        self.book_id = book_id
        self.req_user_id = req_user_id
        self.owner_user_id = owner_user_id

        self.request_date = request_date

    def __repr__(self):
        return "<ID: {0}, REQ_DATE: {1}, ACPT_DATE: {2}, BOOK: {3}, USER: {4}, OWNER: {5}>".format(self.id,
                                                                                                   self.request_date,
                                                                                                   self.accept_date,
                                                                                                   self.book_id,
                                                                                                   self.req_user_id,
                                                                                                   self.owner_user_id)
