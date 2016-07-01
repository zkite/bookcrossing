from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask_sqlalchemy import Model

from bookcrossing.views.books.base_book_view import BaseBookView
from bookcrossing.models.category import CategoryModel, CategorySchema
from bookcrossing.models.book import BookModel


class BaseBookSearchView(BaseBookView):

	def get_category_list(self) -> list or None:
		"""
		Get all categories
		"""
		categories = []
		category_list = CategoryModel.query.all()
		if category_list:
			for category in category_list:
				formed_category = CategorySchema().dump(category).data
				categories.append(formed_category)
			return categories
		else:
			return None

	def search_by_title(self, pattern: str) -> list or None:
		"""
		BookSearch books by title
		"""
		result = BookModel.query.filter(BookModel.title.like('%' + pattern + "%"))
		if result:
			books = []
			for book in result:
				formed_book = self._book_formation(book)
				books.append(formed_book)
			return books
		else:
			return None

	def get_category_object(self, category_name: str) -> Model or None :
		"""
		Get category object by category name
		"""
		try:
			c = CategoryModel.query.filter_by(name=category_name).first()
		except(NoResultFound, MultipleResultsFound):
			return None
		else:
			return c

	def get_books_by_category(self, category_name: str) -> list or None:
		"""
		Get books by category from select form
		"""
		books = []
		category = self.get_category_object(category_name)
		selected_books = BookModel.query.filter_by(category_id=category.id).all()
		if selected_books:
			for book in selected_books:
				formed_book = self._book_formation(book)
				books.append(formed_book)
			return books
		else:
			return None
