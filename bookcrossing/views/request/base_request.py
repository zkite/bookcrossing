from bookcrossing.views.base_view import BaseMethodView
from bookcrossing.models.requests import RequestModel
from bookcrossing.models.user import UserModel
from bookcrossing.models.book import BookModel
from bookcrossing import db


class BaseRequestView(BaseMethodView):
    def create_request(self, request_data: dict, uid: int) -> object or None:
        """
        check Requester User
          -OK
          -ERROR
        change Requester User state (point++)
        create Request Object, save to DB
        """

        if not self._check_user_points(uid):
            return None

        request = self.create_model(RequestModel,
                                    **request_data)
        if not request:
            return None

        if not self._increment_user_points(uid):
            return None

        return request

    def update_request(self, rid: int, request_data: dict) -> object or None:
        """
        change Request state (change Accept date)
        make Book invisible
        """

        request = self.get_model(rid,
                                 RequestModel)
        if not request:
            return None

        if not self._make_book_invisible(request.book_id):
            return None

        request = self.update_model(rid, RequestModel,
                                    request_data)
        if not request:
            return None

        return request

    def delete_request(self, rid: int) -> object or None:
        """
        Remove Request Object
        Make Book visible
        Change Book Owner
        For Old Owner point--
        """

        rem_request = self.delete_model(rid,
                                        RequestModel)
        if not rem_request:
            return None

        if not self._make_book_visible(rem_request.book_id):
            return None

        if not self._change_book_owner(rem_request.book_id,
                                       rem_request.req_user_id):
            return None

        if not self._decrement_user_points(rem_request.owner_user_id):
            return None

        return rem_request

    def get_request(self, rid: int) -> object or None:
        return self.get_model(rid,
                              RequestModel)

    def _check_user_points(self, uid: int) -> bool:
        user = self.get_model(uid,
                              UserModel)
        if not user:
            return False
        if user.points < user.limit:
            return True
        else:
            return False

    def _increment_user_points(self, uid: int) -> bool:
        user = self.get_model(uid,
                              UserModel)
        if not user:
            return False
        user.points += 1
        db.session.add(user)
        db.session.commit()
        return True

    def _decrement_user_points(self, uid: int) -> bool:
        user = self.get_model(uid,
                              UserModel)
        if not user:
            return False
        user.points -= 1
        db.session.add(user)
        db.session.commit()
        return True

    def _make_book_invisible(self, bid: int) -> object or None:
        book = self.get_model(bid,
                              BookModel)
        if not book:
            return None
        book.visible = False
        db.session.add(book)
        db.session.commit()
        return book

    def _make_book_visible(self, bid: int) -> object or None:
        book = self.get_model(bid,
                              BookModel)
        if not book:
            return None
        book.visible = True
        db.session.add(book)
        db.session.commit()
        return book

    def _change_book_owner(self, bid: int, rid: int) -> bool:
        book = self.get_model(bid,
                              BookModel)
        requester = self.get_model(rid,
                                   UserModel)
        if not book or not requester:
            return False
        book.user_id = requester.id
        db.session.add(book)
        db.session.commit()
        return True

    @staticmethod
    def get_income_requests(user_id: int) -> list or None:
        req_list = RequestModel.query.filter_by(owner_user_id=user_id).all()
        if req_list:
            return req_list
        else:
            return None

    @staticmethod
    def get_outcome_requests(user_id: int) -> list or None:
        req_list = RequestModel.query.filter_by(req_user_id=user_id).all()
        if req_list:
            return req_list
        else:
            return None
