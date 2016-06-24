import datetime
from bookcrossing import db
from marshmallow_sqlalchemy import ModelSchema

from bookcrossing.models.book import BookModel

class RequestModel(db.Model):
    __tablename__ = 'requests'

    id = db.Column('id', db.Integer, primary_key=True)
    request_date = db.Column('request_date', db.DateTime, nullable=False)
    accept_date = db.Column('accept_date', db.DateTime, default=None)
    notification_counter = db.Column('notification_counter', db.Integer, default=0)
    book_id = db.Column('book_id', db.Integer, db.ForeignKey('books.id'))
    req_user_id = db.Column('req_user_id', db.Integer, db.ForeignKey('users.id'))
    owner_user_id = db.Column('owner_user_id', db.Integer, db.ForeignKey('users.id'))

    book = db.relationship("BookModel", backref='request')

    def __init__(self, book_id, req_user_id, owner_user_id,
                 request_date=datetime.datetime.now(), accept_date=None):
        self.book_id = book_id
        self.req_user_id = req_user_id
        self.owner_user_id = owner_user_id

        self.request_date = request_date
        self.accept_date = accept_date

    def __repr__(self):
        return "<ID: {0}, REQ_DATE: {1}, ACPT_DATE: {2}, BOOK: {3}, USER: {4}, OWNER: {5}>".format(self.id,
                                                                                                   self.request_date,
                                                                                                   self.accept_date,
                                                                                                   self.book_id,
                                                                                                   self.req_user_id,
                                                                                                   self.owner_user_id)


# for serializing Book model
class RequestSchema(ModelSchema):
    class Meta:
        model = RequestModel
