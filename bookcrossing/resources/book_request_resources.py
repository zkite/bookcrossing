from flask import make_response
from flask_restful import Resource

from bookcrossing.utils.book_request import (create_book_request,
                                             remove_request,
                                             get_book_requests)

from bookcrossing.mail.email import send_email


class BookRequestResource(Resource):
    def get(self, request_id=None):
        book_requests = get_book_requests()
        pass

    def post(self, book_id=None, requester_id=None):

        if not requester_id or not book_id:
            return make_response('requester_id or book_id ADD ERROR')

        book_req = create_book_request(book_id,
                                       requester_id)
        if book_req:
            # TODO change send_email parameters
            send_email('fenderoksp@gmail.com', 'Hello Title', 'Hello MSG BODY')
            send_email('fenderoksp@gmail.com', 'Hello Title', 'Hello MSG BODY')
            return make_response('Book Request OK, MSG SEND')

        else:
            return make_response('Book Req ADD ERROR')

    def delete(self, request_id=None):
        if not request_id:
            return make_response('Request_id DELETE ERROR')

        rem_req = remove_request(request_id)
        if rem_req:
            return make_response('Book Req DELETE OK')

        else:
            return make_response('Book Req DELETE ERROR')
