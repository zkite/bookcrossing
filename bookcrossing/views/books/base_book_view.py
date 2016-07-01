from flask_sqlalchemy import Model
from sqlalchemy.exc import ProgrammingError, IntegrityError
from flask_login import current_user

from bookcrossing import db
from bookcrossing.views.base_view import BaseMethodView
from bookcrossing.models.book import BookModel, BookSchema
from bookcrossing.models.user import UserModel
from bookcrossing.models.category import CategoryModel
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


class BaseBookView(BaseMethodView):
    def create_model(self, book: Model, category: Model, data: dict) -> Model or None:
        """
        Create Book
        """
        b = super().create_model(book, data['title'], data['author'], data['publisher'])
        c = self._is_category_exist(data['category'])
        if not c:
            c = super().create_model(category, data['category'])
        if b and c:
            b.category_id = c.id
            b.user_id = current_user.id
            self._increment_user_points(current_user.id)
            try:
                db.session.commit()
            except(ProgrammingError, IntegrityError):
                return None
            else:
                return b
        else:
            return None

    def make_shelf(self, user_id: int) -> list() or None:
        """
        Make books shelf and reverse it
        """
        shelf = []
        user_book_list = BookModel.query.filter_by(user_id=user_id).all()
        if user_book_list:
            for book in user_book_list:
                formed_book = self._book_formation(book)
                shelf.append(formed_book)
            shelf.reverse()
            return shelf
        else:
            return None

    def _book_formation(self, book: Model) -> list():
        """
        Make book formation
        """
        formed_book = BookSchema().dump(book).data
        formed_book['category'] = self._get_book_category(book)
        formed_book['owner'] = self._get_book_owner(book)
        return formed_book

    def _get_book_category(self, book: Model) -> str or None:
        """
        Get book category
        """
        try:
            c = CategoryModel.query.get(book.category_id)
        except(NoResultFound, MultipleResultsFound):
            return None
        else:
            return c.name

    def _get_book_owner(self, book: Model) -> str or None:
        """
        Get book owner
        """
        try:
            o = UserModel.query.get(book.user_id)
        except(NoResultFound, MultipleResultsFound):
            return None
        else:
            return o.login

    def _is_category_exist(self, category_name: str) -> Model or False:
        try:
            c = CategoryModel.query.filter_by(name=category_name).first()
        except(NoResultFound):
            return False
        else:
            return c

    def update_model(self, model: Model, data: dict) -> Model or None:
        category = self._is_category_exist(data['category'])
        book_id = data.pop('id', None)
        if category and book_id:
            del data['category']
            data['category_id'] = category.id
            updated_book = super().update_model(book_id, BookModel, data)
            return updated_book
        elif not category and book_id:
            category = super().create_model(CategoryModel, data['category'])
            del data['category']
            data['category_id'] = category.id
            updated_book = super().update_model(book_id, BookModel, data)
            return updated_book
        else:
            return None

    def get_book_profile(self, book_id) -> (dict, bool):
        book = self.get_model(book_id, BookModel)
        formed_book = self._book_formation(book)
        owner = False
        if not current_user.is_anonymous:
            owner = current_user.is_owner(book.user_id)
        return (formed_book, owner)

    def get_all_books(self) -> list or None:
        """
        Get all books
        """
        books = []
        book_list = BookModel.query.all()
        if book_list:
            for book in book_list:
                if book.visible:
                    formed_book = self._book_formation(book)
                    books.append(formed_book)
            return books
        else:
            return None

    def _increment_user_points(self, user_id):
        user = UserModel.query.get(user_id)
        user.limit += 1

        db.session.add(user)
        db.session.commit()

        return user