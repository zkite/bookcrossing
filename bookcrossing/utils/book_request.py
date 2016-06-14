import uuid

from bookcrossing.mail.email import send_async_email
from bookcrossing.models.models import (User,
                                        Book,
                                        BookRequest,
                                        db)


def generate_uuid() -> str:
    return str(uuid.uuid4())


def create_book_request(book_id: int, requester_id: int) -> bool:
    requester = User.query.get(requester_id)

    if not requester:
        return False

    if requester.points < requester.limit:
        requester.points += 1
        book = Book.query.get(book_id)
        book_request = BookRequest(book_id, requester_id, book.user_id)

        db.session.add(book_request)
        db.session.add(requester)
        db.session.commit()
        return True

    else:
        return False


def remove_request(request_id: int) -> bool:
    book_request = BookRequest.query.get(request_id)

    if not book_request:
        return False

    book = Book.query.get(book_request.book_id)
    book.user_id = book_request.req_user_id
    book.visible = True

    owner = User.query.get(book_request.owner_user_id)
    owner.points -= 1

    db.session.add(book)
    db.session.add(owner)
    db.session.delete(book_request)
    db.session.commit()
    return True


def send_notification_email_created_book_request(book_id: int, requester_id: int) -> bool:
    requester = User.query.get(requester_id)
    book = Book.query.get(book_id)
    owner = User.query.get(book.id)
    send_async_email(requester.email,
                     'Book Request Created',
                     'email/request_created.html',
                     user=requester)
    send_async_email(owner.email,
                     'Book Request Created',
                     'email/request_created.html',
                     user=owner)
    return True


# TODO Just use other names
def get_requested_book_requests(user_id: int) -> list:
    list_requested_book_requests = BookRequest.query.filter_by(owner_user_id=user_id).all()
    if list_requested_book_requests:
        return list_requested_book_requests
    else:
        return None


def get_sent_book_requests(user_id: int) -> list:
    list_sent_book_requests = BookRequest.query.filter_by(req_user_id=user_id).all()
    if list_sent_book_requests:
        return list_sent_book_requests
    else:
        return None
