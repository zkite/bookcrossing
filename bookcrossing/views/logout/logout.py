from flask import flash, redirect
from flask_login import logout_user, login_required

from bookcrossing.views.logout.logout_base import BaseLogoutView


class LogoutView(BaseLogoutView):

    @staticmethod
    def get():
        logout_user()
        flash('You have been logged out!')
        return redirect('/login')
