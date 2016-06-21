from flask_restful import Resource
from flask_sqlalchemy import Model
from sqlalchemy.exc import ProgrammingError, IntegrityError
from sqlalchemy.orm.exc import ObjectDeletedError, StaleDataError, NoResultFound, MultipleResultsFound
from marshmallow_sqlalchemy import ModelSchema

from bookcrossing.models import db


class BaseResource(Resource):
	def create_model(self, model: Model, *args: list, **kwargs: dict):
		m = model(*args, **kwargs)
		db.session.add(m)
		try:
			db.session.commit()
		except(ProgrammingError, IntegrityError):
			return None
		else:
			return m

	def delete_model(self, model: Model):
		db.session.delete(model)
		try:
			db.session.commit()
		except(ObjectDeletedError, StaleDataError):
			return None
		else:
			model

	def get_model(self, id: int, model: Model):
		try:
			m = model.query.get(id)
		except(NoResultFound, MultipleResultsFound):
			return None
		else:
			return m

	def update_model(self, id: int, model: Model, data: dict):
		m = self.get_model(id, model)
		if m and data:
			for k in data:
				try:
					m.k
				except AttributeError:
					return None
				else:
					m.k = data['k']
			try:
				db.session.commit()
			except(ProgrammingError, IntegrityError):
					return None
			else:
				return m
		else:
			return None

	def serialize_model(self, id: int, model: Model, schema: ModelSchema):
		m = self.get_model(id, model)
		if m:
			serialized_model = schema.dump(m).data
			return serialized_model
		else:
			None


