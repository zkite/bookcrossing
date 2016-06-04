from flask_restful import Resource
from flask import make_response, render_template


# This is just example GET, POST methods working with render_template
class Index(Resource):
    def get(self):
        return make_response(render_template('index.html'))

    def post(self):
        return 'Hello POST'


class Book(Resource):
    def get(self, bookid=None):
        return 'Book Get'

    def post(self, bookid=None):
        return 'Book Post'

    def put(self, bookid=None):
        if bookid:
            return 'Book Put {}'.format(bookid)
        else:
            return 'Book Put List'

    def delete(self, bookid=None):
        if bookid:
            return 'Book {0} Delete'.format(bookid)
        else:
            return 'Book del without bookid'
