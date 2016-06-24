from flask import render_template, flash, redirect
from flask_login import current_user
from bookcrossing.views.user_profile.user_profile_base import BaseUserProfileView
from bookcrossing.forms.edit_profile_form import EditProfileForm
from bookcrossing import db


class UserProfileView(BaseUserProfileView):

    @staticmethod
    def get():
        return render_template('user_profile.html')

    def post(self):
        form = EditProfileForm()
        if form.validate_on_submit():
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.office = form.office.data
            current_user.phone_number = form.phone_number.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your profile has been updated.')
            return redirect('/user_profile')
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.office.data = current_user.office
        form.phone_number.data = current_user.phone_number
        return render_template('edit_profile.html', form=form)



