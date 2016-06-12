from flask_testing import TestCase
from flask import Flask

from config import TestingConfig
from bookcrossing.models.models import (db,
                                        User,
                                        Book,
                                        BookRequest)
from bookcrossing.utils.book_request import (create_book_request,
                                             accept_request)


class TestBookRequest(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config.from_object(TestingConfig)

        db.init_app(app)

        with app.app_context():
            db.create_all()

        return app

    def setUp(self):
        test_user_1 = User('test_user_1_login', 'test_user_1_password', 'test_user_1_email',
                           'test_user_1_first_name', 'test_user_1_last_name', 'Dnepr-1', '1234567890')
        test_user_1.id = 11111

        test_user_2 = User('test_user_2_login', 'test_user_2_password', 'test_user_2_email',
                           'test_user_2_first_name', 'test_user_2_last_name', 'Kiev-1', '0987654321')
        test_user_2.id = 22222
        test_user_2.limit = 2
        test_user_2.points = 1

        test_book_1 = Book('test_book_1_title', 'test_book_1_author',
                           'test_book_1_publisher', 'test_book_1_category')
        test_book_1.id = 12345
        test_book_1.user_id = test_user_1.id

        db.session.add(test_user_1)
        db.session.add(test_user_2)
        db.session.add(test_book_1)
        db.session.commit()

    def test_book_request(self):
        book = Book.query.get(12345)
        requester = User.query.get(22222)
        book_request_bool = create_book_request(book.id, requester.id)

        self.assertEqual(book_request_bool, True)

        book_request = BookRequest.query.get(1)

        self.assertEqual(book_request.book_id, 12345)
        self.assertEqual(book_request.req_user_id, 22222)
        self.assertEqual(book_request.owner_user_id, 11111)

    def test_accept_request(self):
        test_book_request = BookRequest(12345, 22222, 11111)

        owner = User.query.get(11111)
        owner.points = 1

        book = Book.query.get(12345)
        book.visible = False

        db.session.add(test_book_request)
        db.session.commit()

        accept_req_bool = accept_request(test_book_request.id)

        self.assertEqual(accept_req_bool, True)
        self.assertEqual(owner.points, 0)
        self.assertEqual(book.visible, True)
        self.assertEqual(book.user_id, 22222)
        self.assertNotIn(test_book_request, db.session)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
