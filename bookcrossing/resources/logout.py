from flask import session, url_for, redirect
from flask_restful import Resource
from flask_login import logout_user


class Logout(Resource):
	def get(self):
		session.clear()
		logout_user()
		return redirect(url_for('index'))
