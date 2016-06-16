from flask import redirect, render_template, url_for, flash
from flask_login import current_user

from bookcrossing.forms.registration_user import RegistrationForm
from bookcrossing.models.models import User
from bookcrossing.models import db


def edit_user():
    user = current_user
    form = RegistrationForm()

    form.login.data = user.login
    form.email.data = user.email
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.office.data = user.office
    form.phone_number.data = user.phone_number

    return render_template('edit_user_profile.html', form = form)


def update_user():
    user = current_user
    form = RegistrationForm()


    if form.validate_on_submit():
        user.login=form.login.data
        user.email=form.email.data
        user.first_name=form.first_name.data
        user.last_name=form.last_name.data
        user.office=form.office.data
        user.phone_number=form.phone_number.data
        user.password=form.password.data

        db.session.add(user)
        db.session.commit()
        flash('Your profile has been updated!')

        return redirect(url_for('hello'))

    return render_template('edit_user_profile.html', form = form)
