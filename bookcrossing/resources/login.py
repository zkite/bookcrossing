from bookcrossing.models.user import UserModel
from flask import session, url_for, redirect, render_template, request, flash, make_response
from flask_login import login_user
from bookcrossing.forms.login import LoginForm
from flask_restful import Resource
from werkzeug.security import check_password_hash


class Login(Resource):
	form = None
	headers = {'Content-Type': 'text/html'}

	def get(self):
		self.form = LoginForm(request.form)
		if session.get('login'):
			flash('You are already logged in', category="alert alert-info")
		return make_response(render_template('login.html', form=self.form), 200, self.headers)

	def post(self):
		self.form = LoginForm(request.form)
		if self.form.validate():
			login = request.form['login']
			password = request.form['password']
			user = UserModel.query.filter_by(login=login).first()
			print(user)
			if user and check_password_hash(user.password, password):
				session['login'] = login
				login_user(user)
				flash('Logged in successfully', category="alert alert-info")
				return redirect(request.args.get('next') or url_for('index'))
			else:
				flash('You are not registered yet or login/pass are incorect', category="alert alert-danger")
		return make_response(render_template('login.html', form=self.form), 200, self.headers)
