from flask.views import MethodView
from flask_sqlalchemy import Model
from sqlalchemy.exc import ProgrammingError, IntegrityError
from sqlalchemy.orm.exc import ObjectDeletedError, StaleDataError, NoResultFound, MultipleResultsFound
from marshmallow_sqlalchemy import ModelSchema

from bookcrossing import db


class BaseMethodView(MethodView):
    def create_model(self, model: Model, *args: list, **kwargs: dict) -> Model or None:
        m = model(*args, **kwargs)
        db.session.add(m)
        try:
            db.session.commit()
        except(ProgrammingError, IntegrityError):
            return None
        else:
            return m

    def delete_model(self, mid: int, model: Model) -> Model or None:
        m = self.get_model(mid, model)
        if not m:
            return None
        db.session.delete(m)
        try:
            db.session.commit()
        except(ObjectDeletedError, StaleDataError):
            return None
        else:
            return m

    @staticmethod
    def get_model(mid: int, model: Model) -> Model or None:
        try:
            m = model.query.get(mid)
        except(NoResultFound, MultipleResultsFound):
            return None
        else:
            return m

    def update_model(self, mid: int, model: Model, data: dict) -> Model or None:
        m = self.get_model(mid, model)
        if m and data:
            for k in data:
                try:
                    m.k
                except AttributeError:
                    return None
                else:
                    m.k = data['k']

            db.session.add(m)
            try:
                db.session.commit()
            except(ProgrammingError, IntegrityError):
                return None
            else:
                return m
        else:
            return None

    def serialize_model(self, mid: int, model: Model, schema: ModelSchema) -> Model or None:
        m = self.get_model(mid, model)
        if m:
            serialized_model = schema.dump(m).data
            return serialized_model
        else:
            return None
