from flask import make_response, render_template
from flask_restful import Resource
from flask_login import current_user


class ShowProfile(Resource):
    def get(self):
        return make_response(render_template('show_user_profile.html',
                                             user=current_user))
