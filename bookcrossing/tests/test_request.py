import sys
import os
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             '../..'))

from datetime import datetime
from flask import Flask
from flask_testing import TestCase

from bookcrossing import db
from bookcrossing.config import TestingConfig
from bookcrossing.models.user import UserModel
from bookcrossing.models.book import BookModel
from bookcrossing.views.request.base_request import BaseRequestView


class TestRequest(TestCase, BaseRequestView):
    def create_app(self):
        app = Flask(__name__)
        app.config.from_object(TestingConfig)

        db.init_app(app)

        with app.app_context():
            db.create_all()

        return app

    def setUp(self):
        test_user_1 = UserModel('test_user_1_login', 'test_user_1_password', 'test_user_1_email',
                                'test_user_1_first_name', 'test_user_1_last_name', 'Dnepr-1', '1234567890')
        test_user_1.id = 11111
        test_user_1.limit = 2
        test_user_1.points = 1

        test_user_2 = UserModel('test_user_2_login', 'test_user_2_password', 'test_user_2_email',
                                'test_user_2_first_name', 'test_user_2_last_name', 'Kiev-1', '0987654321')
        test_user_2.id = 22222
        test_user_2.limit = 2
        test_user_2.points = 1

        test_book_1 = BookModel('test_book_1_title', 'test_book_1_author',
                                'test_book_1_publisher')
        test_book_1.id = 12345
        test_book_1.user_id = test_user_1.id

        db.session.add(test_user_1)
        db.session.add(test_user_2)
        db.session.add(test_book_1)
        db.session.commit()

    def test_create_request(self):
        book = self.get_model(12345, BookModel)
        requester = self.get_model(22222, UserModel)
        data = {'book_id': book.id,
                'req_user_id': requester.id,
                'owner_user_id': book.user_id}
        book_request_test_1 = self.create_request(uid=requester.id,
                                                  request_data=data)

        self.assertIn(book_request_test_1, db.session)

        book_request = self.get_request(1)

        self.assertNotEqual(book_request, None)
        self.assertEqual(book_request.book_id, 12345)
        self.assertEqual(book_request.req_user_id, 22222)
        self.assertEqual(book_request.owner_user_id, 11111)
        self.assertEqual(requester.limit, 2)
        self.assertEqual(requester.points, 2)

        # can't create request because of user points check
        book_request_test_2 = self.create_request(uid=requester.id,
                                                  request_data=data)

        self.assertEqual(book_request_test_2, None)
        self.assertEqual(requester.points, requester.limit)

    def test_update_request(self):
        book = self.get_model(12345, BookModel)
        requester = self.get_model(22222, UserModel)
        data = {'book_id': book.id,
                'req_user_id': requester.id,
                'owner_user_id': book.user_id}
        book_request_test_1 = self.create_request(uid=requester.id,
                                                  request_data=data)
        data = {'accept_date': datetime.now()}
        datetime_now = datetime.now()
        book_request_test_2 = self.update_request(rid=book_request_test_1.id,
                                                  request_data=data)

        self.assertIn(book_request_test_2, db.session)

        book_request = self.get_request(1)

        self.assertEqual(book_request.accept_date.strftime("%Y-%m-%d %H:%M"),
                         datetime_now.strftime("%Y-%m-%d %H:%M"))

    def test_delete_request(self):
        book = self.get_model(12345, BookModel)
        requester = self.get_model(22222, UserModel)
        owner = self.get_model(book.user_id, UserModel)

        data = {'book_id': book.id,
                'req_user_id': requester.id,
                'owner_user_id': book.user_id}
        book_request_test_1 = self.create_request(uid=requester.id,
                                                  request_data=data)

        book_request_test_1 = self.delete_request(book_request_test_1.id)

        self.assertNotEqual(book_request_test_1, None)
        self.assertNotIn(book_request_test_1, db.session)
        self.assertEqual(book.user_id, requester.id)
        self.assertNotEqual(book.user_id, owner.id)
        self.assertEqual(owner.points, 0)
        self.assertEqual(book.visible, True)

    def test_get_request(self):
        book = self.get_model(12345, BookModel)
        requester = self.get_model(22222, UserModel)
        data = {'book_id': book.id,
                'req_user_id': requester.id,
                'owner_user_id': book.user_id}
        book_request_test_1 = self.create_request(uid=requester.id,
                                                  request_data=data)

        request_test = self.get_request(book_request_test_1.id)
        self.assertIn(request_test, db.session)
        self.assertNotEqual(request_test, None)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    import unittest
    unittest.main()
