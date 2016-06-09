from flask_restful import Resource
from flask import make_response, render_template


# This is just example GET, POST methods working with render_template
class Index(Resource):
    def get(self):
        return make_response(render_template('index.html'), 200)

    def post(self):
        return ['Hello POST']
