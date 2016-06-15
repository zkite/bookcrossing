from flask import make_response, render_template
from flask_restful import Resource
from flask_login import current_user

from bookcrossing.utils.get_user_profile import get_user_books


class ShowProfile(Resource):
    def get(self):
        user = current_user
        books = get_user_books(user.id)
        if user:
            return make_response(render_template('show_user_profile.html',
                                                 user=user,
                                                 books=books))
        else:
            return make_response('OOps there some mistake')
