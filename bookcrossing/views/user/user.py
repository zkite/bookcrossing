from flask import flash, render_template, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash

from bookcrossing.views.user.user_base import BaseUsersView
from bookcrossing.forms.register_form import RegistrationForm
from bookcrossing.forms.login_form import LoginForm
from bookcrossing.forms.restore_password_form import RestorePasswordForm
from bookcrossing.models.user_model import UserModel


from bookcrossing.email.email import send_async_email
from bookcrossing.forms.edit_profile_form import EditProfileForm


class RegistrationView(BaseUsersView):

    @staticmethod
    def get():
        form = RegistrationForm()
        return render_template('registration.html', form=form)

    def post(self):
        form = RegistrationForm()
        if form.validate_on_submit():
            user = self.form_to_user(form)
            self.create_model(UserModel, **user)

            flash('You can now login.')
            flash('A confirmation email has been sent to you by email.')

            send_async_email(form.email.data,
                             'Your Account in Bookcrossing',
                             'email/greeting',
                             first_name=form.first_name.data)

            return redirect('/login/')
        return render_template('registration.html', form=form)


class LoginView(BaseUsersView):

    @staticmethod
    def get():
        form = LoginForm()
        return render_template('login.html', form=form)

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            flag, user = self.verify_user(form)
            if flag:
                login_user(user, form.remember_me.data)
                return redirect(request.args.get('next') or '/profile/')
            flash('Invalid username or password.')
        return render_template('login.html', form=form)


class LogoutView(BaseUsersView):

    @staticmethod
    @login_required
    def get():
        logout_user()
        flash('You have been logged out!')
        return redirect('/login')


class UsersListView(BaseUsersView):

    @staticmethod
    @login_required
    def get():
        users_list = UserModel.query.all()
        return render_template('users.html', users=users_list)


class UserProfileView(BaseUsersView):

    @login_required
    def get(self, user_id=None):
        if user_id is None:
            return render_template('user_profile.html')
        else:
            user = self.get_model(user_id, UserModel)
            return render_template('user_info.html', user=user)


class EditUserProfileView(BaseUsersView):

    @staticmethod
    def get():
        form = EditProfileForm()
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.office.data = current_user.office
        form.phone_number.data = current_user.phone_number
        return render_template('edit_profile.html', form=form)

    def post(self):
        form = EditProfileForm()
        if form.validate_on_submit():

            user_dict = self.form_to_edit(form)

            self.update_model(current_user.id, UserModel, user_dict)

            flash('Your profile has been updated.')
            return redirect('/profile/')
        return render_template('edit_profile.html', form=form)


class RestorePasswordView(BaseUsersView):

    @staticmethod
    def get():
        form = RestorePasswordForm()
        return render_template('restore_password.html', form=form)

    def post(self):
        form = RestorePasswordForm()
        if form.validate_on_submit():

            user = UserModel.query.filter_by(email=form.email.data).first()

            if form.login.data != user.login:
                flash('Invalid username or email.')
                return redirect('/restore/')

            password_hash = generate_password_hash(form.password.data)
            user_dict = {
                'password_hash': password_hash
            }
            self.update_model(user.id, UserModel, user_dict)

            flash('A new password has been sent to you by email.')

            send_async_email(user.email,
                             'New password',
                             'email/restore',
                             user=user,
                             password=form.password.data)

            return redirect('/login/')
        return render_template('restore_password.html', form=form)
