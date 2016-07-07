from datetime import datetime
from flask import request, render_template
from flask_login import current_user, login_required

import logging
import logging.config

from bookcrossing.views.request.base_request import BaseRequestView
from bookcrossing.models.book import BookModel
from bookcrossing.email.email import send_async_email
from bookcrossing.models.user import UserModel
from bookcrossing.config import LOGGING

logging.config.dictConfig(LOGGING)


class RequestView(BaseRequestView):

    @login_required
    def get(self):
        select_category = request.values.get('select')
        logging.debug('GET.Selected category: {}'.format(select_category))
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
            logging.error('RequestView POST book_id ERROR')
            return 'Book ID Error'
        if not current_user:
            logging.error('RequestView POST current_user ERROR')
            return 'Current User Error'
        book = self.get_model(book_id,
                              BookModel)
        logging.info('Book:{}'.format(book))
        if not book:
            logging.error('RequestView POST Book ERROR')
            return 'Book Request Error'
        data = {'book_id': book.id,
                'req_user_id': current_user.id,
                'owner_user_id': book.user_id}
        book_request = self.create_request(request_data=data,
                                           uid=current_user.id)
        logging.info('Book request:{}'.format(book_request))
        if not book_request:
            logging.error('RequestView POST book_request ERROR')
            return 'Book Request Error'

        send_async_email(to=current_user.email,
                         subject='Hello From Request',
                         template='email/outcome-request-notify',
                         user=current_user,
                         book=book)

        owner = self.get_model(book.user_id, UserModel)
        logging.info('Owner is:{}'.format(owner))
        send_async_email(to=owner.email,
                         subject='Hello From Request',
                         template='email/outcome-request-notify',
                         user=owner,
                         book=book)

        logging.info('RequestView POST book_request OK')
        return 'Book Request was created successfully'

    @login_required
    def put(self, request_id=None):
        if not request_id:
            logging.error('RequestView PUT request_id ERROR')
            return 'Book Request ID Error'
        data = {'accept_date': datetime.now()}
        update_request = self.update_request(rid=request_id,
                                             request_data=data)
        logging.info('Updated request:{}'.format(update_request))
        if not update_request:
            logging.error('RequestView PUT update_request ERROR')
            return 'Update Request Error'
        logging.info('RequestView PUT update_request OK')
        return 'Book Request was updated successfully'

    @login_required
    def delete(self, request_id=None):
        if not request_id:
            logging.error('RequestView DELETE request_id ERROR')
            return 'Book Request ID Error'
        history_request = self._create_request_history(request_id)
        delete_request = self.delete_request(rid=request_id)
        logging.info('Deleted request:{}'.format(delete_request))
        logging.info('History request:{}'.format(history_request))
        if not delete_request:
            logging.error('RequestView DELETE delete_request ERROR')
            return 'Book Request was not deleted successfully'
        logging.info('RequestView DELETE delete_request OK')
        return 'Book Request was deleted successfully'


class DeclineRequestView(BaseRequestView):

    @login_required
    def post(self, request_id=None):
        if not request_id:
            logging.error('DeclineRequestView POST request_id ERROR')
            return 'Book Request ID ERROR'
        declined_request = self.decline_request(request_id)
        if not declined_request:
            logging.error('DeclineRequestView POST declined_request ERROR')
            return 'Decline Request Error'
        logging.info('DeclineRequestView POST OK')
        return 'Book Request was declined successfully'
