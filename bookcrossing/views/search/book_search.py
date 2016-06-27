from flask import render_template, request

from bookcrossing.views.search.base_book_search import BaseBookSearchView
from bookcrossing.forms.search import SearchForm


class BookSearchView(BaseBookSearchView):
    def get(self):
        categories = self.get_category_list()
        books = self.get_all_books()
        if books:
            return render_template('search.html', books=books, categories=categories)
        else:
            return render_template('search.html', categories=categories)

    def post(self):
        categories = self.get_category_list()
        form = SearchForm(request.form)
        if form.validate():
            if form.search.data:
                books = self.search_by_title(form.search.data)
                if books:
                    return render_template('search.html', books=books, categories=categories)
            else:
                return render_template('search.html', categories=categories)

        if form.select.data:
            books = self.get_books_by_category(form.select.data)
            if books:
                return render_template('search.html', books=books, categories=categories, select_category=form.select.data)
            else:
                return render_template('search.html', categories=categories)
        else:
            return render_template('search.html', categories=categories)
