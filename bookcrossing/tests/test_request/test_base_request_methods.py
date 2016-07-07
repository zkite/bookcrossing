import sys
import os
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             '../..'))

from flask_testing import TestCase

from bookcrossing import db, app
from bookcrossing.config import TestingConfig
from bookcrossing.models.user import UserModel
from bookcrossing.models.book import BookModel
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
        test_user_1.limit = 2
        test_user_1.points = 1

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

    def test_check_user_points(self):
        res = self._check_user_points(11111)
        self.assertEqual(res, True)

    def test_increment_user_points(self):
        res = self._increment_user_points(11111)
        self.assertEqual(res, True)

    def test_decrement_user_points(self):
        res = self._decrement_user_points(11111)
        self.assertEqual(res, True)

    def test_make_book_visible(self):
        book = BookModel.query.get(12345)
        book.visible = False
        self._make_book_visible(bid=book.id)
        self.assertEqual(book.visible, True)

    def test_make_book_invisible(self):
        book = BookModel.query.get(12345)
        book.visible = True
        self._make_book_invisible(bid=book.id)
        self.assertEqual(book.visible, False)

    def test_change_book_owner(self):
        book = BookModel.query.get(12345)
        requester = UserModel.query.get(22222)
        res = self._change_book_owner(bid=book.id,
                                      rid=requester.id)
        self.assertEqual(res, True)
        self.assertEqual(book.user_id, requester.id)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    import unittest
    unittest.main()
