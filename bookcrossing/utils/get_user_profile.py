from bookcrossing.models.models import Book


def get_user_books(user_id: int) -> list:
    books = Book.query.filter_by(user_id=user_id).all()
    if not books:
        return None
    else:
        return books
