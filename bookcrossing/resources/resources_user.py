from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required

from bookcrossing.models import db
from bookcrossing.forms.registration_user import (RegistrationForm,
                                                  LoginForm)

from bookcrossing.models.models import User
from bookcrossing.mail.email import send_email


def hello():
    users = User.query.all()
    return render_template('index.html', users=users)


def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(login=form.login.data,
                    email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    office=form.office.data,
                    phone_number=form.phone_number.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        flash('A confirmation email has been sent to you by email.')
        # send_email(user.email, 'Your Account in BookCros', user.last_name)
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('hello'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('hello'))
