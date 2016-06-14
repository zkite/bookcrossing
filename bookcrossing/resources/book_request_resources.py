from flask import make_response, render_template
from flask_restful import Resource

from bookcrossing.utils.book_request import (create_book_request,
                                             remove_request,
                                             get_requested_book_requests,
                                             get_sent_book_requests,
                                             send_notification_email_created_book_request)


class BookRequestResource(Resource):

    def get(self, user_id=None):

        if not user_id:
            return make_response('User_id ERROR')
        requested = get_requested_book_requests(user_id)
        sent_requests = get_sent_book_requests(user_id)
        if requested and sent_requests:
            return make_response(render_template('user_requests.html',
                                                 requested=requested,
                                                 sent_requests=sent_requests))
        else:
            return make_response('OOps No Requests Today')

    def post(self, book_id=None, requester_id=None):
        if not requester_id or not book_id:
            return make_response('requester_id or book_id ADD ERROR')
        book_req = create_book_request(book_id,
                                       requester_id)
        if book_req:
            send_notification_email_created_book_request(book_id,
                                                         requester_id)
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
