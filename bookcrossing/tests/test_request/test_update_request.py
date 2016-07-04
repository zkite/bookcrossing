import sys
import os

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             '../..'))

from datetime import datetime
from flask import Flask
from flask_testing import TestCase

from bookcrossing import db
from bookcrossing.config import TestingConfig
from bookcrossing.models.book import BookModel
from bookcrossing.models.requests import RequestModel
from bookcrossing.views.request.base_request import BaseRequestView


class TestRequest(TestCase):
    test_request = BaseRequestView()

    def create_app(self):
        app = Flask(__name__)
        app.config.from_object(TestingConfig)
        db.init_app(app)
        with app.app_context():
            db.create_all()
        return app

    def setUp(self):
        book_test_1 = BookModel(title='test_book_1_title',
                                author='test_book_1_author',
                                publisher='test_book_1_publisher')
        book_test_1.id = 12345
        book_test_1.user_id = 11111

        book_request_test_1 = RequestModel(book_id=12345,
                                           req_user_id=22222,
                                           owner_user_id=11111)
        book_request_test_1.id = 55555

        book_request_test_2 = RequestModel(book_id=12345,
                                           req_user_id=22222,
                                           owner_user_id=11111)
        book_request_test_2.id = 66666

        book_request_test_3 = RequestModel(book_id=12345,
                                           req_user_id=22222,
                                           owner_user_id=11111)
        book_request_test_3.id = 77777

        book_request_test_4 = RequestModel(book_id=12345,
                                           req_user_id=22222,
                                           owner_user_id=11111)
        book_request_test_4.id = 88888

        db.session.add(book_request_test_1)
        db.session.add(book_request_test_2)
        db.session.add(book_request_test_3)
        db.session.add(book_request_test_4)
        db.session.add(book_test_1)
        db.session.commit()

    def test_update_request(self):
        book = BookModel.query.get(12345)
        data = {'accept_date': datetime.now()}
        book_request_test_1 = TestRequest.test_request.update_request(rid=55555,
                                                                      request_data=data)

        self.assertNotEqual(book_request_test_1, None)
        self.assertIn(book_request_test_1, db.session)
        self.assertEqual(book.visible, False)
        self.assertEqual(book_request_test_1.accept_date, data['accept_date'])

    def test_delete_not_approved_requests(self):
        book_request_test_1 = RequestModel.query.get(66666)
        book_request_test_2 = RequestModel.query.get(77777)
        book_request_test_3 = RequestModel.query.get(88888)
        res = TestRequest.test_request._delete_not_approved_requests(book_id=12345)

        self.assertEqual(res, True)
        self.assertNotIn(book_request_test_1, db.session)
        self.assertNotIn(book_request_test_2, db.session)
        self.assertNotIn(book_request_test_3, db.session)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    import unittest

    unittest.main()
