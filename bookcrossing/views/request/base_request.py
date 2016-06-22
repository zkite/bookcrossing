from bookcrossing.views.base_view import BaseMethodView
from bookcrossing.models.requests import RequestModel
from bookcrossing.models.user import UserModel
from bookcrossing import db


class BaseRequestView(BaseMethodView):
    def create_request(self, request_data: dict, uid: int) -> object or None:
        check_points = BaseRequestView._check_user_points(uid)
        if not check_points:
            return None

        BaseRequestView._increment_user_points(uid)
        return self.create_model(RequestModel, **request_data)

    def update_request(self, rid: int, request_data: dict) -> object or None:
        return self.update_model(rid, RequestModel, request_data)

    def delete_request(self, rid: int) -> object or None:
        return self.delete_model(rid, RequestModel)

    def get_request(self, rid: int) -> object or None:
        return self.get_model(rid, RequestModel)

    @staticmethod
    def _get_user(uid: int) -> object or None:
        user = UserModel.query.get(uid)
        if user:
            return user
        else:
            return None

    @staticmethod
    def _check_user_points(uid: int) -> bool:
        user = BaseRequestView._get_user(uid)
        if not user:
            return False

        if user.points < user.limit:
            return True
        else:
            return False

    @staticmethod
    def _increment_user_points(uid: int) -> bool:
        user = BaseRequestView._get_user(uid)
        if not user:
            return False

        user.points += 1

        db.session.add(user)
        db.session.commit()

        return True

    @staticmethod
    def _decrement_user_points(uid: int) -> bool:
        user = BaseRequestView._get_user(uid)
        if not user:
            return False

        user.points -= 1

        db.session.add(user)
        db.session.commit()

        return True
