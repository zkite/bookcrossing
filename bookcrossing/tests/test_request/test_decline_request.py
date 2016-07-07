import sys
import os

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             '../..'))

from flask_testing import TestCase

from bookcrossing import db, app
from bookcrossing.config import TestingConfig
from bookcrossing.models.user import UserModel
from bookcrossing.models.book import BookModel
from bookcrossing.models.requests import RequestModel
from bookcrossing.views.request.base_request import BaseRequestView


class TestRequest(TestCase, BaseRequestView):
    def create_app(self, app=app):
        app.config.from_object(TestingConfig)
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
        test_user_2.points = 1

        book_test_1 = BookModel(title='test_book_1_title',
                                author='test_book_1_author',
                                publisher='test_book_1_publisher')
        book_test_1.id = 12345
        book_test_1.user_id = test_user_1.id

        book_request_test_1 = RequestModel(book_id=12345,
                                           req_user_id=22222,
                                           owner_user_id=11111)
        book_request_test_1.id = 55555

        db.session.add(book_request_test_1)
        db.session.add(book_test_1)
        db.session.add(test_user_1)
        db.session.add(test_user_2)
        db.session.commit()

    def test_decline_request(self):
        requester = UserModel.query.get(22222)
        book_request_test_1 = self.decline_request(55555)
        self.assertNotEqual(book_request_test_1, None)
        self.assertNotIn(book_request_test_1, db.session)
        self.assertEqual(requester.points, 0)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    import unittest
    unittest.main()
