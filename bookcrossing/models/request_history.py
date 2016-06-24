import datetime
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import event

from bookcrossing import db
from bookcrossing.models.requests import RequestModel


class RequestHistoryModel(db.Model):
    __tablename__ = 'request_history'

    id = db.Column('id', db.Integer, primary_key=True)
    request_date = db.Column('request_date', db.DateTime, nullable=False)
    accept_date = db.Column('accept_date', db.DateTime, default=None)
    notification_counter = db.Column('notification_counter', db.Integer, default=0)
    book_title = db.Column('book_title', db.String(60))
    req_user_login = db.Column('req_user_login', db.String(30))
    owner_user_login = db.Column('owner_user_login', db.String(30))

    def __init__(self, book_title, req_user_login, owner_user_login,
                 request_date=None, accept_date=None):
        self.book_title = book_title
        self.req_user_login = req_user_login
        self.owner_user_id = owner_user_login

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


@event.listens_for(RequestModel, 'after_delete')
def receive_after_delete(mapper, connection, target):
    req_hist_obj = RequestHistoryModel(target.book.title, target.req_user.login, target.owner_user.login,
                                       target.request_date, target.accept_date)
    db.session.add(req_hist_obj)
    db.session.commit()
