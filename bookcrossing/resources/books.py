from flask_restful import Resource
from flask import make_response, render_template, url_for, redirect
from bookcrossing.models.models import (db,
                                        Book,
                                        Category)
from bookcrossing.forms.books import BookForm

def index():
    books = Book.query.all()
    template = render_template('books/index.html', books=books)
    return make_response(template, 200)

def show(book_id):
    book = Book.query.filter_by(id=book_id).first()
    template = render_template('books/show.html', book=book)
    return make_response(template, 200)

def new():
    # populate categories for development
    categories = [Category(name) for name in ['Fantasy', 'Adventure', 'Drama', 'Crime']]
    for c in categories:
        db.session.add(c)
    db.session.commit()

    form = BookForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by('name')]

    if form.validate_on_submit():
        category = Category.query.filter_by(id=form.category_id.data).first()
        book = Book(title=form.title.data,
                    author=form.author.data,
                    publisher=form.publisher.data,
                    category=category)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('books.show', book_id=book.id))

    template = render_template('books/new.html', form=form)
    return make_response(template, 200)

def edit(book_id):
    categories = [Category(name) for name in ['Fantasy', 'Adventure', 'Drama', 'Crime']]
    db.session.add_all(categories)
    db.session.commit()

    book = Book.query.filter_by(id=book_id).first()

    form = BookForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by('name')]

    form.title.data = book.title
    form.author.data = book.author
    form.publisher.data = book.publisher
    form.category_id.data = book.category_id

    template = render_template('books/edit.html', form=form)
    return make_response(template, 200)

def update(book_id):
    categories = [Category(name) for name in ['Fantasy', 'Adventure', 'Drama', 'Crime']]
    db.session.add_all(categories)
    db.session.commit()

    book = Book.query.filter_by(id=book_id).first()

    form = BookForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by('name')]

    if form.validate_on_submit():
        book.title=form.title.data
        book.author=form.author.data
        book.publisher=form.publisher.data
        book.category_id=form.category_id.data

        db.session.add(book)
        db.session.commit()
        return redirect(url_for('books.show', book_id=book.id))

    template = render_template('books/edit.html', form=form)
    return make_response(template, 200)