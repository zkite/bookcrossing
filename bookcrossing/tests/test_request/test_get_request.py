import sys
import os

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             '../..'))

from flask import Flask
from flask_testing import TestCase

from bookcrossing import db
from bookcrossing.config import TestingConfig
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
        book_request_test_1 = RequestModel(book_id=12345,
                                           req_user_id=22222,
                                           owner_user_id=11111)
        book_request_test_1.id = 55555

        db.session.add(book_request_test_1)
        db.session.commit()

    def test_get_request(self):
        request_test = TestRequest.test_request.get_request(55555)

        self.assertIn(request_test, db.session)
        self.assertNotEqual(request_test, None)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    import unittest

    unittest.main()
