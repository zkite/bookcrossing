from bookcrossing.models.book import BookModel, BookSchema
from bookcrossing.models.category import CategoryModel, CategorySchema
from bookcrossing.models.user import UserModel

from flask import render_template, request, make_response
from bookcrossing.forms.search import SearchForm
from flask_restful import Resource

from bookcrossing.utils.book_utils import get_book_category, get_book_owner, book_formation, \
    get_category_list, search_books, get_books_by_category, get_all_books


class Search(Resource):
    def __init__(self):
        self.headers = {'Content-Type': 'text/html'}

    def get(self):
        categories = get_category_list(CategoryModel, CategorySchema())
        books = get_all_books(BookModel, BookSchema(), get_book_category, get_book_owner, book_formation, CategoryModel,
                              UserModel)
        if books:
            return make_response(render_template('search.html', books=books, categories=categories), 200)
        else:
            return make_response(render_template('search.html', categories=categories), 200)

    def post(self):
        self.form = SearchForm(request.form)
        search_form = self.form.search.data
        select_form = self.form.select.data

        categories = get_category_list(CategoryModel, CategorySchema())

        if self.form.validate():
            if search_form:
                books = search_books(search_form, BookModel, get_book_category, get_book_owner, book_formation,
                                     BookSchema(), CategoryModel, UserModel)
                if books:
                    return make_response(render_template('search.html', books=books, categories=categories), 200,
                                         self.headers)
            else:
                return make_response(render_template('search.html', categories=categories), 200, self.headers)

        if select_form:
            books = get_books_by_category(select_form, CategoryModel, BookModel, BookSchema(), get_book_owner,
                                          get_book_category, book_formation, UserModel)
            if books:
                return make_response(render_template('search.html', books=books, categories=categories), 200,
                                     self.headers)
            else:
                return make_response(render_template('search.html', categories=categories), 200, self.headers)
        else:
            return make_response(render_template('search.html', categories=categories), 200, self.headers)
