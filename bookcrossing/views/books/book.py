import json

from flask import render_template, request
from flask_login import current_user, login_required

from bookcrossing.views.books.base_book_view import BaseBookView
from bookcrossing.models.book import BookModel
from bookcrossing.models.category import CategoryModel
from bookcrossing.forms.book import AddBookForm, UpdateBookForm


class BooksView(BaseBookView):
    @login_required
    def get(self):
        """
        Get all books from database
        """
        form = AddBookForm(request.form)
        shelf = self.make_shelf(current_user.id)
        return render_template('books.html', form=form.data, shelf=shelf)

    @login_required
    def post(self):
        """
        Create book
        """
        form = AddBookForm(request.form)
        if form.validate():
            self.create_model(BookModel, CategoryModel, form.data)
            shelf = self.make_shelf(current_user.id)
            return render_template('books.html', form=form.data, shelf=shelf)
        else:
            return json.dumps(form.errors)

    @login_required
    def put(self):
        """
        Update book
        """
        form = UpdateBookForm(request.form)
        if form.validate():
            self.update_model(BookModel, form.data)
            shelf = self.make_shelf(current_user.id)
            return render_template('books.html', form=form.data, shelf=shelf)
        else:
            return json.dumps(form.errors)

    @login_required
    def delete(self):
        """
        Delete book
        """
        book = request.get_json()
        self.delete_model(book['id'], BookModel)
        return json.dumps({'delete': 'ok', 'id': book['id']})


class BookProfileView(BaseBookView):
    def get(self, book_id):
        book, owner = self.get_book_profile(book_id)
        return render_template('book_profile.html', book_id=book_id, book=book, owner=owner)
