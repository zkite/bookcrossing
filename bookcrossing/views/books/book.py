import json
import logging
import logging.config


from flask import render_template, request
from flask_login import current_user, login_required

from bookcrossing.views.books.base_book_view import BaseBookView
from bookcrossing.models.book import BookModel
from bookcrossing.models.category import CategoryModel
from bookcrossing.forms.book import AddBookForm, UpdateBookForm
from bookcrossing.config import LOGGING

logging.config.dictConfig(LOGGING)


class BooksView(BaseBookView):
    @login_required
    def get(self):
        """
        Get all books from database
        """
        form = AddBookForm(request.form)
        shelf = self.make_shelf(current_user.id)
        return render_template('books.html', form=form.data, shelf=shelf), \
               logging.debug('Hello from GET. '
                             'All books of {} have been shown.'
                             .format(current_user.login))

    @login_required
    def post(self):
        """
        Create book
        """
        form = AddBookForm(request.form)
        if form.validate():
            logging.debug('Hello from POST. Add book form validated.')
            self.create_model(BookModel, CategoryModel, form.data)
            shelf = self.make_shelf(current_user.id)
            return render_template('books.html', form=form.data, shelf=shelf), \
                   logging.debug('Hello from POST. Book created.'
                                 'All books of {} have been shown.'
                                 .format(current_user.login))
        else:
            return json.dumps(form.errors), \
                   logging.error('Hello from POST. Errors.')

    @login_required
    def put(self):
        """
        Update book
        """
        form = UpdateBookForm(request.form)
        if form.validate():
            logging.debug('Hello from PUT. Update book form validated.')
            self.update_model(BookModel, form.data)
            shelf = self.make_shelf(current_user.id)
            return render_template('books.html', form=form.data, shelf=shelf), \
                   logging.debug('Hello from PUT. Book updated.'
                                 'All books of {} have been shown.'
                                 .format(current_user.login))
        else:
            return json.dumps(form.errors), \
                   logging.error('Hello from PUT. Errors.')

    @login_required
    def delete(self):
        """
        Delete book
        """
        book = request.get_json()
        self.delete_model(book['id'], BookModel)
        return json.dumps({'delete': 'ok', 'id': book['id']}), \
               logging.debug('Hello from DELETE. Errors.')


class BookProfileView(BaseBookView):
    def get(self, book_id):
        book, owner = self.get_book_profile(book_id)
        return render_template('book_profile.html', book_id=book_id, book=book, owner=owner), \
               logging.debug('Hello from GET. Book {} profile template rendered.'
                             .format(book.title))
