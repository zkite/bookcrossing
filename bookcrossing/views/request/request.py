from datetime import datetime
from flask_login import current_user
import logging
import logging.config

from bookcrossing.views.request.base_request import BaseRequestView
from bookcrossing.models.book import BookModel
from bookcrossing.config import LOGGING

logging.config.dictConfig(LOGGING)


class RequestView(BaseRequestView):
    def get(self, request_id=None):
        if not request_id:
            logging.error('RequestView GET request_id ERROR')
        request_obj = self.get_request(request_id)
        logging.info('Request:{}'.format(request_obj))
        if not request_obj:
            logging.error('RequestView GET request_obj ERROR')
        logging.info('RequestView GET request_obj OK')

    def post(self, book_id=None):
        if not book_id:
            logging.error('RequestView POST book_id ERROR')
        if not current_user:
            logging.error('RequestView POST current_user ERROR')
        book = self.get_model(book_id,
                              BookModel)
        logging.info('Book:{}'.format(book))
        if not book:
            logging.error('RequestView POST Book ERROR')
        data = {'book_id': book.id,
                'req_user_id': current_user.id,
                'owner_user_id': book.user_id}
        book_request = self.create_request(request_data=data,
                                           uid=current_user.id)
        logging.info('Book request:{}'.format(book_request))
        if not book_request:
            logging.error('RequestView POST book_request ERROR')
        logging.info('RequestView POST book_request OK')

    def put(self, request_id=None):
        if not request_id:
            logging.error('RequestView PUT request_id ERROR')
        data = {'accept_date': datetime.now()}
        update_request = self.update_request(rid=request_id,
                                             request_data=data)
        logging.info('Updated request:{}'.format(update_request))
        if not update_request:
            logging.error('RequestView PUT update_request ERROR')
        logging.info('RequestView PUT update_request OK')

    def delete(self, request_id=None):
        if not request_id:
            logging.error('RequestView DELETE request_id ERROR')
        delete_request = self.delete_request(rid=request_id)
        logging.info('Deleted request:{}'.format(delete_request))
        if not delete_request:
            logging.error('RequestView DELETE delete_request ERROR')
        logging.info('RequestView DELETE delete_request OK')
