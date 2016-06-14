from bookcrossing.models.models import (User,
                                        Book)


def get_user(user_id: int) -> object:
    user = User.query.get(user_id)
    if not user:
        return None
    else:
        return user


def get_user_books(user_id: int) -> list:
    books = Book.query.filter_by(user_id=user_id).all()
    if not books:
        return None
    else:
        return books
