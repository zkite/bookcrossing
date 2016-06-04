# create your models here
from sqlalchemy import String, Integer
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

OWNER = {'Dima': 1, 'Alex': 2}


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(Integer, primary_key=True)
    id_owner = OWNER
    title = db.Column(String(length=256))
    author = db.Column(String(length=256))
    category = db.Column(String(length=256))

    def __repr__(self):
        return '<Book id: {0}, title: {1}, author: {2}>'.format(self.id,
                                                                self.title,
                                                                self.author)
