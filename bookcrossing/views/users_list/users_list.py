from flask import render_template
from bookcrossing.models.user_model import UserModel
from bookcrossing.views.users_list.users_list_base import BaseUsersListView


class UsersListView(BaseUsersListView):
    @staticmethod
    def get():
        users_list = UserModel.query.all()
        return render_template('users.html', users=users_list)
