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
from bookcrossing.models.requests import RequestModel
from bookcrossing.models.request_history import RequestHistoryModel
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

        test_request_1 = RequestModel(12345, 22222, 11111, accept_date=datetime.now())
        test_request_1.id = 33333

        db.session.add(test_user_1)
        db.session.add(test_user_2)
        db.session.add(test_book_1)
        db.session.add(test_request_1)
        db.session.commit()

    def test_create_request_history(self):
        request = self.get_model(33333,
                                   RequestModel)

        count_before = db.session.query(RequestHistoryModel).count()

        db.session.delete(request)
        # db.session.commit()

        count_after = db.session.query(RequestHistoryModel).count()

        self.assertEqual(count_after, count_before + 1)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    import unittest
    unittest.main()
