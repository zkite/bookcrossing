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


class TestRequest(TestCase, BaseRequestView):
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

        db.session.add(book_request_test_1)
        db.session.add(book_test_1)
        db.session.commit()

    def test_update_request(self):
        data = {'accept_date': datetime.now()}
        book_request_test_1 = self.update_request(rid=55555,
                                                  request_data=data)

        self.assertNotEqual(book_request_test_1, None)
        self.assertIn(book_request_test_1, db.session)
        self.assertEqual(book_request_test_1.accept_date.strftime("%Y-%m-%d %H:%M"),
                         datetime.now().strftime("%Y-%m-%d %H:%M"))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    import unittest
    unittest.main()
