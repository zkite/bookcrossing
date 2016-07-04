import sys
import os
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             '../..'))

from flask import Flask
from flask_testing import TestCase

from bookcrossing import db
from bookcrossing.config import TestingConfig
from bookcrossing.models.user import UserModel
from bookcrossing.models.book import BookModel
from bookcrossing.models.requests import RequestModel
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
        test_user_1 = UserModel(login='test_user_1_login',
                                password='test_user_1_password',
                                email='test_user_1_email',
                                first_name='test_user_1_first_name',
                                last_name='test_user_1_last_name',
                                office='Dnepr-1',
                                phone_number='1234567890')
        test_user_1.id = 11111

        test_user_2 = UserModel(login='test_user_2_login',
                                password='test_user_2_password',
                                email='test_user_2_email',
                                first_name='test_user_2_first_name',
                                last_name='test_user_2_last_name',
                                office='Kiev-1',
                                phone_number='0987654321')
        test_user_2.id = 22222
        test_user_2.limit = 2
        test_user_2.points = 1

        test_book_1 = BookModel(title='test_book_1_title',
                                author='test_book_1_author',
                                publisher='test_book_1_publisher')
        test_book_1.id = 12345
        test_book_1.user_id = test_user_1.id

        db.session.add(test_user_1)
        db.session.add(test_user_2)
        db.session.add(test_book_1)
        db.session.commit()

    def test_create_request(self):
        book = BookModel.query.get(12345)
        requester = UserModel.query.get(22222)

        data = {'book_id': book.id,
                'req_user_id': requester.id,
                'owner_user_id': book.user_id}
        book_request_test_1 = self.create_request(uid=requester.id,
                                                  request_data=data)

        self.assertNotEqual(book_request_test_1, None)
        self.assertIn(book_request_test_1, db.session)
        self.assertEqual(book_request_test_1.book_id, 12345)
        self.assertEqual(book_request_test_1.req_user_id, 22222)
        self.assertEqual(book_request_test_1.owner_user_id, 11111)
        self.assertEqual(requester.limit, 2)
        self.assertEqual(requester.points, 2)

    def test_create_request_points_fail(self):
        # can't create request because of user points check
        book = BookModel.query.get(12345)
        requester = UserModel.query.get(22222)
        requester.limit = 1

        data = {'book_id': book.id,
                'req_user_id': requester.id,
                'owner_user_id': book.user_id}
        book_request_test_1 = self.create_request(uid=requester.id,
                                                  request_data=data)

        self.assertEqual(book_request_test_1, None)
        self.assertEqual(requester.points, requester.limit)

    def test_create_request_existing_req_check(self):
        test_req = RequestModel(book_id=12345,
                                req_user_id=22222,
                                owner_user_id=11111)
        db.session.add(test_req)
        db.session.commit()

        book = BookModel.query.get(12345)
        requester = UserModel.query.get(22222)
        data = {'book_id': book.id,
                'req_user_id': requester.id,
                'owner_user_id': book.user_id}
        book_request_test_1 = self.create_request(uid=requester.id,
                                                  request_data=data)

        self.assertEqual(book_request_test_1, None)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    import unittest
    unittest.main()
