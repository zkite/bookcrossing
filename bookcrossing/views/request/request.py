from datetime import datetime
from flask import request, render_template
from flask_login import current_user, login_required

from bookcrossing.views.request.base_request import BaseRequestView
from bookcrossing.models.book import BookModel
from bookcrossing.email.email import send_async_email
from bookcrossing.models.user import UserModel


class RequestView(BaseRequestView):

    @login_required
    def get(self):
        select_category = request.values.get('select')
        requests = None
        if select_category:
            requests = self.get_requests_by_category(category=select_category,
                                                     current_user_id=current_user.id)

        return render_template('requests.html',
                               requests=requests,
                               category=select_category,
                               user=current_user)

    @login_required
    def post(self, book_id=None):
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

        send_async_email(to=current_user.email,
                         subject='Hello From Request',
                         template='email/outcome-request-notify',
                         user=current_user,
                         book=book)

        owner = self.get_model(book.user_id, UserModel)
        send_async_email(to=owner.email,
                         subject='Hello From Request',
                         template='email/request-notify',
                         user=owner,
                         book=book)

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
        history_request = self._create_request_history(request_id)
        delete_request = self.delete_request(rid=request_id)
        print(history_request)
        if not delete_request:
            return 'RequestView DELETE delete_request ERROR'
        return 'RequestView DELETE delete_request OK'


class DeclineRequestView(BaseRequestView):

    @login_required
    def post(self, request_id=None):
        if not request_id:
            return 'DeclineRequestView POST request_id ERROR'
        declined_request = self.decline_request(request_id)
        if not declined_request:
            return 'DeclineRequestView POST declined_request ERROR'
        return 'DeclineRequestView POST OK'
