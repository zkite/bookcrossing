import logging
import logging.config

from flask import flash, render_template, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash

from bookcrossing.views.user.user_base import BaseUsersView
from bookcrossing.forms.register_form import RegistrationForm
from bookcrossing.forms.login_form import LoginForm
from bookcrossing.forms.restore_password_form import RestorePasswordForm
from bookcrossing.models.user import UserModel


from bookcrossing.email.email import send_async_email
from bookcrossing.forms.edit_profile_form import EditProfileForm
from bookcrossing.config import LOGGING

logging.config.dictConfig(LOGGING)

class RegistrationView(BaseUsersView):

    @staticmethod
    def get():
        form = RegistrationForm()
        logging.debug('GET. Registration form rendered.')
        return render_template('registration.html', form=form)



    def post(self):
        form = RegistrationForm()
        if form.validate_on_submit():
            logging.debug('Registration template validated.')
            user = self.form_to_user(form)
            self.create_model(UserModel, **user)
            logging.debug('User {} created.'.format(user['login']))

            flash('You can now login.')
            flash('A confirmation email has been sent to you by email.')

            send_async_email(form.email.data,
                             'Your Account in Bookcrossing',
                             'email/greeting',
                             first_name=form.first_name.data)
            logging.debug('Email to {} sended.'.format(user['email']))
            logging.debug('User {} registered and can login.'
                          .format(user['login']))

            return redirect('/login/')

        logging.debug('User entered invalid values on submit. '
                      'Registration template rendered again.')
        return render_template('registration.html', form=form)



class LoginView(BaseUsersView):

    @staticmethod
    def get():
        form = LoginForm()
        logging.debug('Registration form rendered.')
        return render_template('login.html', form=form)


    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            logging.debug('Login form validated.')
            flag, user = self.verify_user(form)
            if flag:
                logging.debug('User {} is in DB.'.format(user.login))
                login_user(user, form.remember_me.data)
                logging.debug('User {} is logged in and redirected.'
                              .format(user.login))
                return redirect(request.args.get('next') or '/profile/')

            flash('Invalid username or password.')
            logging.debug('User entered invalid values on submit. '
                          'Login form rendered again.')
        return render_template('login.html', form=form)




class LogoutView(BaseUsersView):

    @staticmethod
    @login_required
    def get():
        logout_user()
        logging.debug('User is logged out.')
        flash('You have been logged out!')
        logging.debug('Redirection to /login.')
        return redirect('/login')


class UsersListView(BaseUsersView):

    @staticmethod
    @login_required
    def get():
        users_list = UserModel.query.all()
        logging.debug('All users list shown.')
        return render_template('users.html', users=users_list)




class UserProfileView(BaseUsersView):

    @login_required
    def get(self, user_id=None):
        if user_id is None:
            logging.debug('User {} profile page has been rendered.'
                          .format(current_user.login))
            return render_template('user_profile.html')

        else:
            user = self.get_model(user_id, UserModel)
            logging.debug('User {} info page has been rendered.'
                          .format(user.login))
            return render_template('user_info.html', user=user)



class EditUserProfileView(BaseUsersView):

    @staticmethod
    def get():
        form = EditProfileForm()
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.office.data = current_user.office
        form.phone_number.data = current_user.phone_number
        logging.debug('Edit profile page has been rendered.')
        return render_template('edit_profile.html', form=form)


    def post(self):
        form = EditProfileForm()
        if form.validate_on_submit():
            logging.debug('Edit profile form has been validated.')
            user_dict = self.form_to_edit(form)

            self.update_model(current_user.id, UserModel, user_dict)

            flash('Your profile has been updated.')
            logging.debug('User {} profile has been updated.'
                          .format(current_user.login))
            logging.debug('User has been redirected to profile page.')
            return redirect('/profile/')
        logging.error('User entered invalid values on submit. '
                      'Edit profile form rendered again.')
        return render_template('edit_profile.html', form=form)


class RestorePasswordView(BaseUsersView):

    @staticmethod
    def get():
        form = RestorePasswordForm()
        logging.debug('Restore password page has been rendered.')
        return render_template('restore_password.html', form=form)


    def post(self):
        form = RestorePasswordForm()
        if form.validate_on_submit():

            logging.debug('Restore password form has been validated.')
            user = UserModel.query.filter_by(email=form.email.data).first()

            if form.login.data != user.login:
                flash('Invalid username or email.')
                logging.error('User {} entered invalid username or email.'
                              .format(current_user.login))
                logging.error('User {} has been redirected to restore page.'
                              .format(current_user.login))
                return redirect('/restore/')

            password_hash = generate_password_hash(form.password.data)
            user_dict = {
                'password_hash': password_hash
            }
            self.update_model(user.id, UserModel, user_dict)

            flash('A new password has been sent to you by email.')

            logging.debug('A new password has been sent to {} by email.'
                          .format(current_user.login))
            send_async_email(user.email,
                             'New password',
                             'email/restore',
                             user=user,
                             password=form.password.data)
            logging.debug('User {} has been redirected to login page.'
                          .format(current_user.login))
            return redirect('/login/')

        logging.debug('User entered invalid values on submit. '
                      'Restore password page rendered again.')
        return render_template('restore_password.html', form=form)


