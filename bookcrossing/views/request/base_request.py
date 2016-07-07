from bookcrossing.models.request_history import RequestHistoryModel
from bookcrossing.views.base_view import BaseMethodView
from bookcrossing.models.requests import RequestModel, RequestSchema
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

        if self._check_existing_requests(uid=uid, book_id=request_data['book_id']):
            return None

        request = self.create_model(RequestModel,
                                    **request_data)
        if not request:
            return None

        if not self._increment_user_points(uid):
            self.delete_model(request.id,
                              RequestModel)
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

        request = self.update_model(rid,
                                    RequestModel,
                                    request_data)
        if not request:
            return None

        if not self._delete_not_approved_requests(request.book_id):
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

    def decline_request(self, rid: int) -> object or None:
        """
        change Requester User state (point--)
        delete Request Object
        """

        request = self.delete_model(rid,
                                    RequestModel)
        if not request:
            return None

        if not self._decrement_user_points(request.req_user_id):
            return None

        return request

    def _check_user_points(self, uid: int) -> bool:
        user = self.get_model(uid,
                              UserModel)
        if not user:
            return False
        return user.points < user.limit

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

    def _delete_not_approved_requests(self, book_id: int) -> list:
        requests_list = RequestModel.query.filter_by(book_id=book_id,
                                                     accept_date=None).all()
        for request in requests_list:
            self.decline_request(request.id)
        return True

    def _create_request_history(self, req_id: int) -> object:
        req = RequestModel.query.get(req_id)
        return self.create_model(RequestHistoryModel,
                                 book_id=req.book_id,
                                 req_user_id=req.req_user_id,
                                 owner_user_id=req.owner_user_id,
                                 request_date=req.request_date,
                                 accept_date=req.accept_date)

    @staticmethod
    def _check_existing_requests(uid: int, book_id: int) -> bool:
        res = RequestModel.query.filter_by(req_user_id=uid,
                                           book_id=book_id).all()
        return bool(res)

    @staticmethod
    def get_requests_by_category(category: str, current_user_id: int) -> list:
        requests = list()
        request_list = None
        if category == 'incoming':
            request_list = RequestModel.query.filter_by(owner_user_id=current_user_id).all()
        if category == 'outcoming':
            request_list = RequestModel.query.filter_by(req_user_id=current_user_id).all()

        for req in request_list:
            parsed_requests = RequestSchema().dump(req).data
            parsed_requests['title'] = BookModel.query.get(req.book_id).title
            parsed_requests['request_date'] = req.request_date.strftime("%y-%m-%d-%H-%M")
            if req.accept_date:
                parsed_requests['accept_date'] = req.accept_date.strftime("%y-%m-%d-%H-%M")
            else:
                parsed_requests['accept_date'] = None
            parsed_requests['requester'] = UserModel.query.get(req.req_user_id).login
            parsed_requests['accepter'] = UserModel.query.get(req.owner_user_id).login
            requests.append(parsed_requests)

        return requests

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
