from flask import make_response, render_template
from flask_restful import Resource

from bookcrossing.utils.get_user_profile import get_user, get_user_books


class ShowProfile(Resource):
    def get(self, user_id=None):
        user = get_user(user_id)
        books = get_user_books(user_id)
        if user and books:
            return make_response(render_template('show_user_profile.html',
                                                 user=user,
                                                 books=books))
        else:
            return make_response('OOps there some mistake')
