from flask import make_response
from flask_restful import Resource

from bookcrossing.utils.book_request import (create_book_request,
                                             send_email_notification)


class BookRequestResource(Resource):

    def post(self, book_id=None, requester_id=None):

        if not requester_id or not book_id:
            return ['Some problem with owner id or requester id or book id!']

        book_req = create_book_request(book_id,
                                       requester_id)
        if book_req:
            send_email_notification('fenderoksp@gmail.com', 'Hello Title', 'Hello MSG BODY')
            send_email_notification('fenderoksp@gmail.com', 'Hello Title', 'Hello MSG BODY')
            return make_response('Book Request OK, MSG SEND')

        else:
            return make_response('Book Req ERROR')
