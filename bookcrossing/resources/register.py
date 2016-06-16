from bookcrossing import db
from bookcrossing.models.user import UserModel
from flask import session, url_for, redirect, render_template, request, flash, make_response
from bookcrossing.forms.register import RegistrationForm
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from bookcrossing.email.email import send_async_email

class Register(Resource):

	def __init__(self):
		self.headers = {'Content-Type': 'text/html'}

	def get(self):
		self.form = RegistrationForm(request.form)
		if session.get('username'):
			flash('You are already logged in')
		return make_response(render_template('register.html', form=self.form), 200, self.headers)

	def post(self):
		self.form = RegistrationForm(request.form)
		if self.form.validate():
			login = self.form.login.data
			email = self.form.email.data
			first_name = self.form.first_name.data
			last_name = self.form.last_name.data
			office = self.form.office.data
			phone = self.form.phone.data
			password = self.form.password.data

			existing_user = UserModel.query.filter_by(login=login).first()
			if existing_user:
				flash('This login has been already taken. Try another one', category='alert alert-danger')
				return make_response(render_template('register.html', form=self.form), 200, self.headers)

			existing_email = UserModel.query.filter_by(email=email).first()
			if existing_email:
				flash('This email has been already taken. Try another one', category='alert alert-danger')
				return make_response(render_template('register.html', form=self.form), 200, self.headers)

			user = UserModel(login, generate_password_hash(password), email, first_name, last_name, office, phone)
			db.session.add(user)
			db.session.commit()

			flash('User successfully registered', category="alert alert-info")

			send_async_email(user.email, 'Your Account in BookCros', user.first_name)

			return redirect(url_for('login'))
		return make_response(render_template('register.html', form=self.form), 200, self.headers)

