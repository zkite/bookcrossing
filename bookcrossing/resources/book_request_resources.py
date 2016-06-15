from flask import make_response, render_template
from flask_restful import Resource

from bookcrossing.utils.book_request import (create_book_request,
                                             remove_request,
                                             get_requested_book_requests,
                                             get_sent_book_requests,
                                             send_notification_email_created_book_request)

from bookcrossing.models.models import *


class BookRequestResource(Resource):
    def get(self, user_id=None):
        ##################################################################
        test_user_1 = User('test_user_1_login', 'test_user_1_password', 'test_user_1_email',
                           'test_user_1_first_name', 'test_user_1_last_name', 'Dnepr-1', '1234567890')
        test_user_1.id = 11111
        test_user_1.limit = 3
        test_user_1.points = 1

        test_user_2 = User('test_user_2_login', 'test_user_2_password', 'test_user_2_email',
                           'test_user_2_first_name', 'test_user_2_last_name', 'Kiev-1', '0987654321')
        test_user_2.id = 22222
        test_user_2.limit = 2
        test_user_2.points = 1

        test_book_1 = Book('test_book_1_title', 'test_book_1_author',
                           'test_book_1_publisher', 'test_book_1_category')
        test_book_2 = Book('test_book_2_title', 'test_book_2_author',
                           'test_book_2_publisher', 'test_book_2_category')
        test_book_1.id = 12345
        test_book_1.user_id = test_user_1.id
        test_book_2.user_id = test_user_2.id

        db.session.add(test_user_1)
        db.session.add(test_user_2)
        db.session.add(test_book_1)
        db.session.add(test_book_2)
        db.session.commit()

        create_book_request(test_book_1.id, test_user_2.id)
        create_book_request(test_book_2.id, test_user_1.id)
        #######################################################################################
        if not user_id:
            return make_response('User_id ERROR')
        requested = get_requested_book_requests(user_id)
        sent_requests = get_sent_book_requests(user_id)
        return make_response(render_template('user_requests.html',
                                             requested=requested,
                                             sent_requests=sent_requests))

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
