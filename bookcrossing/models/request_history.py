import datetime
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import event

from bookcrossing import db
from bookcrossing.models.requests import RequestModel
from bookcrossing.models.book import BookModel
from bookcrossing.models.user import UserModel


class RequestHistoryModel(db.Model):
    __tablename__ = 'request_history'

    id = db.Column('id', db.Integer, primary_key=True)
    request_date = db.Column('request_date', db.DateTime, nullable=False)
    accept_date = db.Column('accept_date', db.DateTime, default=None)
    notification_counter = db.Column('notification_counter', db.Integer, default=0)

    book_title = db.Column('book_title', db.String(60))
    book_author = db.Column('book_author', db.String(80))
    book_publisher = db.Column('book_publisher', db.String(40))
    book_category = db.Column('book_category', db.String(20))

    req_user_login = db.Column('req_user_login', db.String(30))
    req_user_email = db.Column('req_user_email', db.String(60))
    req_user_first_name = db.Column('req_user_first_name', db.String(30))
    req_user_last_name = db.Column('req_user_last_name', db.String(30))
    req_user_office = db.Column('req_user_office', db.String(20))
    req_user_phone_number = db.Column('req_user_phone_number', db.String(20))

    owner_user_login = db.Column('owner_user_login', db.String(30))
    owner_user_email = db.Column('owner_user_email', db.String(60))
    owner_user_first_name = db.Column('owner_user_first_name', db.String(30))
    owner_user_last_name = db.Column('owner_user_last_name', db.String(30))
    owner_user_office = db.Column('owner_user_office', db.String(20))
    owner_user_phone_number = db.Column('owner_user_phone_number', db.String(20))

    def __init__(self, book_id, req_user_id, owner_user_id,
                 request_date=None, accept_date=None):
        book = BookModel.query.get(book_id)
        self.book_title = book.title
        self.book_author = book.author
        self.book_publisher = book.publisher
        self.book_category = book.category

        req_user = UserModel.query.get(req_user_id)
        self.req_user_login = req_user.login
        self.req_user_email = req_user.email
        self.req_user_first_name = req_user.first_name
        self.req_user_last_name = req_user.last_name
        self.req_user_office = req_user.office
        self.req_user_phone_number = req_user.phone_number

        owner_user = UserModel.query.get(owner_user_id)
        self.owner_user_login = owner_user.login
        self.owner_user_email = owner_user.email
        self.owner_user_first_name = owner_user.first_name
        self.owner_user_last_name = owner_user.last_name
        self.owner_user_office = owner_user.office
        self.owner_user_phone_number = owner_user.phone_number

        self.request_date = request_date
        self.accept_date = accept_date

    def __repr__(self):
        return "<ID: {0}, REQ_DATE: {1}, ACPT_DATE: {2}, BOOK: {3}, USER: {4}, OWNER: {5}>".format(self.id,
                                                                                                   self.request_date,
                                                                                                   self.accept_date,
                                                                                                   self.book_title,
                                                                                                   self.req_user_login,
                                                                                                   self.owner_user_login)

# for serializing Book model
class RequestSchema(ModelSchema):
    class Meta:
        model = RequestHistoryModel
