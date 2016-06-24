from datetime import datetime
from flask_login import current_user
import logging
import logging.handlers

from bookcrossing.views.request.base_request import BaseRequestView
from bookcrossing.models.book import BookModel

###############################################
####           LOGGING SETTINGS            ####
###############################################

f = logging.Formatter(fmt='%(levelname)s:%(name)s: %(message)s '
    '(%(asctime)s; %(filename)s:%(lineno)d)',
    datefmt="%Y-%m-%d %H:%M:%S")
handlers = [
    logging.handlers.RotatingFileHandler('rotated.log', encoding='utf8',
        maxBytes=100000, backupCount=1),
    logging.StreamHandler()
]
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
for h in handlers:
    h.setFormatter(f)
    h.setLevel(logging.DEBUG)
    root_logger.addHandler(h)

###############################################
####         END LOGGING SETTINGS          ####
###############################################

class RequestView(BaseRequestView):
    def get(self, request_id=None):
        if not request_id:
            logging.error('RequestView GET request_id ERROR')
            return 'RequestView GET request_id ERROR'
        request_obj = self.get_request(request_id)
        if not request_obj:
            logging.error('RequestView GET request_id ERROR')
            return 'RequestView GET request_obj ERROR'
        logging.error('RequestView GET request_obj OK')
        return 'RequestView GET request_obj OK'

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
        return 'RequestView POST book_request OK'

    def put(self, request_id=None):
        if not request_id:
            return 'RequestView PUT request_id ERROR'
        data = {'accept_date': datetime.now()}
        update_request = self.update_request(rid=request_id,
                                             request_data=data)
        if not update_request:
            return 'RequestView PUT update_request ERROR'
        return 'RequestView PUT update_request OK'

    def delete(self, request_id=None):
        if not request_id:
            return 'RequestView DELETE request_id ERROR'
        delete_request = self.delete_request(rid=request_id)
        if not delete_request:
            return 'RequestView DELETE delete_request ERROR'
        return 'RequestView DELETE delete_request OK'
