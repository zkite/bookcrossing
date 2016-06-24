from flask import flash, render_template, redirect, request
from flask_login import login_user

from bookcrossing.views.login.login_base import BaseLoginView
from bookcrossing.forms.login_form import LoginForm


class LoginView(BaseLoginView):

    @staticmethod
    def get():
        form = LoginForm()
        return render_template('login.html', form=form)

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            flag, user = self.verify_user(form)
            if flag:
                login_user(user)
                return redirect(request.args.get('next') or '/user_profile')
            flash('Invalid username or password.')
        return render_template('login.html', form=form)

    def put(self):
        pass

    def delete(self):
        pass
