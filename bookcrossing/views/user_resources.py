from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user

from bookcrossing import db
from bookcrossing.forms.register_form import RegistrationForm
from bookcrossing.forms.login_form import LoginForm
from bookcrossing.forms.edit_profile_form import EditProfileForm

from bookcrossing.models.user import UserModel
from bookcrossing.email.email import send_async_email


def index():
    return render_template('index.html')


def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = UserModel(login=form.login.data,
                         email=form.email.data,
                         first_name=form.first_name.data,
                         last_name=form.last_name.data,
                         office=form.office.data,
                         phone_number=form.phone.data,
                         password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        flash('A confirmation email has been sent to you by email.')
        send_async_email(user.email,
                         'Your Account in Bookcrossing',
                         'email/greeting',
                         user=user)
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(login=form.login.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('user_profile'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))


@login_required
def user_profile():
    return render_template('user_profile.html')


@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.office = form.office.data
        current_user.phone_number = form.phone_number.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('user_profile', username=current_user.login))
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.office.data = current_user.office
    form.phone_number.data = current_user.phone_number
    return render_template('edit_profile.html', form=form)

