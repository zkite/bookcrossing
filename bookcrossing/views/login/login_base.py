from bookcrossing.models.user_model import UserModel
from bookcrossing.views.base_view import BaseMethodView


class BaseLoginView(BaseMethodView):

    @staticmethod
    def verify_user(form):
        user = UserModel.query.filter_by(login=form.login.data).first()
        if user is not None and user.verify_password(form.password.data):
            return True, user
        return False, user
