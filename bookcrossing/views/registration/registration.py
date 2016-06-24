from flask import flash, url_for, render_template, redirect

from bookcrossing.email.email import send_async_email
from bookcrossing.forms.register_form import RegistrationForm
from bookcrossing.models.user_model import UserModel
from bookcrossing.views.registration.registration_base import BaseRegistrationView


class RegistrationView(BaseRegistrationView):

    @staticmethod
    def get():
        form = RegistrationForm()
        return render_template('registration.html', form=form)

    def post(self):
        form = RegistrationForm()
        if form.validate_on_submit():

            user = BaseRegistrationView.form_to_user(form)
            self.create_model(UserModel, **user)

            flash('You can now login.')
            flash('A confirmation email has been sent to you by email.')

            send_async_email(form.email.data,
                             'Your Account in Bookcrossing',
                             'email/greeting',
                             first_name=form.first_name.data)

            return redirect('/login')
        return render_template('registration.html', form=form)

    def put(self):
        pass

    def delete(self):
        pass