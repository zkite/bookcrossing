from bookcrossing import db
from marshmallow_sqlalchemy import ModelSchema

class OfficeModel(db.Model):
    __tablename__ = 'offices'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(20), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Office: {0}>".format(self.name)
