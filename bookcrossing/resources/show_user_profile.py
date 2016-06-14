from flask import make_response, render_template
from flask_restful import Resource

from bookcrossing.utils.get_user_profile import get_user, get_user_books

from bookcrossing.models.models import (User, Book, db)


class ShowProfile(Resource):
    def get(self, user_id=None):

        ###############################################
        test_user_1 = User('test_user_1_login', 'test_user_1_password', 'test_user_1_email',
                           'test_user_1_first_name', 'test_user_1_last_name', 'Dnepr-1', '1234567890')
        test_book_1 = Book('test_book_1_title', 'test_book_1_author',
                           'test_book_1_publisher', 'test_book_1_category')
        test_book_2 = Book('test_book_2_title', 'test_book_2_author',
                           'test_book_2_publisher', 'test_book_2_category')
        test_book_1.user_id = 1
        test_book_2.user_id = 1

        db.session.add(test_user_1)
        db.session.add(test_book_1)
        db.session.add(test_book_2)
        db.session.commit()
        ###############################################

        user = get_user(user_id)
        books = get_user_books(user_id)
        if user:
            return make_response(render_template('show_user_profile.html',
                                                 user=user,
                                                 books=books))
        else:
            return make_response('OOps there some mistake')
