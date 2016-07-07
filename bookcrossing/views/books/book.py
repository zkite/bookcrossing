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
        logging.debug('GET. All books of {} have been shown.'
                      .format(current_user.login))
        return render_template('books.html', form=form.data, shelf=shelf)


    @login_required
    def post(self):
        """
        Create book
        """
        form = AddBookForm(request.form)
        print(request.form)
        if form.validate():
            logging.debug('POST. Add book form validated.')
            self.create_model(BookModel, CategoryModel, form.data)
            shelf = self.make_shelf(current_user.id)
            logging.debug('Hello from POST. Book created.'
                          'All books of {} have been shown.'
                          .format(current_user.login))
            return render_template('books.html', form=form.data, shelf=shelf)

        else:
            logging.error('Hello from POST. Creation book error.')
            return json.dumps(form.errors)

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
            logging.debug('Hello from PUT. Book updated.'
                          'All books of {} have been shown.'
                          .format(current_user.login))
            return render_template('books.html', form=form.data, shelf=shelf)

        else:
            logging.error('Hello from PUT. Update book error.')
            return json.dumps(form.errors)

    @login_required
    def delete(self):
        """
        Delete book
        """
        book = request.get_json()
        self.delete_model(book['id'], BookModel)
        logging.debug('DELETE. Book deletion error.')
        return json.dumps({'delete': 'ok', 'id': book['id']})


class BookProfileView(BaseBookView):
    def get(self, book_id):
        book, owner = self.get_book_profile(book_id)
        logging.debug('Hello from GET. Book {} profile template rendered.'
                      .format(book['title']))
        return render_template('book_profile.html', book_id=book_id, book=book, owner=owner)
