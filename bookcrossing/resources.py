from flask_restful import Resource
from flask import make_response, render_template

from bookcrossing.models import Book
from bookcrossing.forms import BookFrom


# This is just example GET, POST methods working with render_template
class Index(Resource):
    def get(self):
        return make_response(render_template('index.html'))

    def post(self):
        return 'Hello POST'


class BookRes(Resource):
    def get(self, bookid=None):
        return make_response(render_template('index.html'))

    def post(self, bookid=None):
        return 'Book Post'

    def put(self, bookid=None):
        queryset = Book
        return make_response(render_template('index.html'))

    def delete(self, bookid=None):
        if bookid:
            return 'Book {0} Delete'.format(bookid)
        else:
            return 'Book del without bookid'
