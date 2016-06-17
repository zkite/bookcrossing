import json

from flask import render_template, request, make_response
from flask_login import current_user, login_required
from flask_restful import Resource

from bookcrossing import db
from bookcrossing.models.book import BookModel, BookSchema
from bookcrossing.models.category import CategoryModel
from bookcrossing.models.user import UserModel
from bookcrossing.forms.book import AddBookForm, UpdateBookForm
from bookcrossing.resources.books.book_utils import make_shelf, get_book_category, get_book_owner, book_formation, update_book, \
    is_category_exist, create_book, get_book_by_id, delete_book_by_id


class BooksResource(Resource):
    def __init__(self):
        self.headers = {'Content-Type': 'text/html'}

    @login_required
    def get(self):
        """
        Get all books from database
        """
        self.form = AddBookForm(request.form)

        make_shelf(BooksResource,
                   BookModel,
                   BookSchema(),
                   get_book_category,
                   get_book_owner,
                   book_formation,
                   CategoryModel,
                   UserModel,
                   current_user)

        return make_response(render_template('books.html', form=self.form, shelf=self.shelf),
                             200,
                             self.headers)

    @login_required
    def post(self):
        """
        Create book object
        """
        self.form = AddBookForm(request.form)
        if self.form.validate():
            title = self.form.title.data
            author = self.form.author.data
            publisher = self.form.publisher.data
            category = self.form.category.data

            category_object = is_category_exist(category,
                                                CategoryModel,
                                                db)

            create_book(BookModel,
                        title,
                        author,
                        publisher,
                        current_user,
                        category_object,
                        db)

            make_shelf(BooksResource,
                       BookModel,
                       BookSchema(),
                       get_book_category,
                       get_book_owner,
                       book_formation,
                       CategoryModel,
                       UserModel,
                       current_user)

            return make_response(render_template('books.html', form=self.form, shelf=self.shelf),
                                 200,
                                 self.headers)
        else:
            return json.dumps(self.form.errors)

    @login_required
    def put(self):
        self.form = UpdateBookForm(request.form)

        if self.form.validate():
            id = self.form.id.data
            title = self.form.title.data
            author = self.form.author.data
            publisher = self.form.publisher.data
            category = self.form.category.data

            book_object = get_book_by_id(BookModel,
                                         id)

            category_object = is_category_exist(category,
                                                CategoryModel,
                                                db)

            update_book(book_object,
                        title,
                        author,
                        publisher,
                        category_object,
                        db)

            make_shelf(BooksResource,
                       BookModel,
                       BookSchema(),
                       get_book_category,
                       get_book_owner,
                       book_formation,
                       CategoryModel,
                       UserModel,
                       current_user)

            return make_response(render_template('books.html', form=self.form, shelf=self.shelf),
                                 200,
                                 self.headers)
        else:
            return json.dumps(self.form.errors)

    @login_required
    def delete(self):
        """ Delete book """
        book = request.get_json()
        delete_book_by_id(BookModel, book['id'], db)
        return {'delete': 'ok', 'id': book['id']}


class BookProfileResource(Resource):
    def __init__(self):
        self.headers = {"Content-Type": "text/html"}

    def get(self, id):
        is_owner = None
        book_object = get_book_by_id(BookModel, id)
        book = book_formation(book_object, BookSchema(), get_book_category, get_book_owner, CategoryModel, UserModel)
        if not current_user.is_anonymous:
            is_owner = current_user.is_owner(book_object.user_id)
        print(book)
        return make_response(render_template('book_profile.html', book=book, owner=is_owner),
                             200,
                             self.headers)
