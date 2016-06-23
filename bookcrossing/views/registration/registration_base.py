from bookcrossing.views.base_view import BaseMethodView


class BaseRegistrationView(BaseMethodView):

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
