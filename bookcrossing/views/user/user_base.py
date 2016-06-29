from bookcrossing.views.base_view import BaseMethodView
from bookcrossing.models.user_model import UserModel


class BaseUsersView(BaseMethodView):

    @staticmethod
    def verify_user(form):
        user = UserModel.query.filter_by(login=form.login.data).first()
        if user is not None and user.verify_password(form.password.data):
            return True, user
        return False, user

    @staticmethod
    def form_to_user(form):
        user_dict = {
            'login': form.login.data,
            'email': form.email.data,
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'office': form.office.data,
            'phone_number': form.phone_number.data,
            'password': form.password.data
        }
        return user_dict

    @staticmethod
    def form_to_edit(form):
        user_dict = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'office': form.office.data,
            'phone_number': form.phone_number.data,
        }
        return user_dict
