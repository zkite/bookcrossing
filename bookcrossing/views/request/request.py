from datetime import datetime
from flask import request, render_template
from flask_login import current_user, login_required

from bookcrossing.views.request.base_request import BaseRequestView

from bookcrossing.models.user import UserModel
from bookcrossing.models.book import BookModel
from bookcrossing.models.requests import RequestModel, RequestSchema


def get_requests_by_category(category):
    requests = list()
    request_list = None
    if category == 'incoming':
        request_list = RequestModel.query.filter_by(owner_user_id=current_user.id).all()
    if category == 'outcoming':
        request_list = RequestModel.query.filter_by(req_user_id=current_user.id).all()

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


class RequestView(BaseRequestView):
    @login_required
    def get(self):
        select_category = request.values.get('select')
        requests = None
        if select_category:
            requests = get_requests_by_category(select_category)

        return render_template('requests.html',
                               requests=requests,
                               category=select_category,
                               user=current_user)

    @login_required
    def post(self, book_id):
        if not book_id:
            return 'RequestView POST book_id ERROR'
        if not current_user:
            return 'RequestView POST current_user ERROR'
        book = self.get_model(book_id,
                              BookModel)
        if not book:
            return 'RequestView POST Book ERROR'
        data = {'book_id': book.id,
                'req_user_id': current_user.id,
                'owner_user_id': book.user_id}
        book_request = self.create_request(request_data=data,
                                           uid=current_user.id)
        if not book_request:
            return 'RequestView POST book_request ERROR'
        return 'RequestView POST book_request OK'

    @login_required
    def put(self, request_id=None):
        if not request_id:
            return 'RequestView PUT request_id ERROR'
        data = {'accept_date': datetime.now()}
        update_request = self.update_request(rid=request_id,
                                             request_data=data)
        if not update_request:
            return 'RequestView PUT update_request ERROR'
        return 'RequestView PUT update_request OK'

    @login_required
    def delete(self, request_id=None):
        if not request_id:
            return 'RequestView DELETE request_id ERROR'
        delete_request = self.delete_request(rid=request_id)
        if not delete_request:
            return 'RequestView DELETE delete_request ERROR'
        return 'RequestView DELETE delete_request OK'
