import uuid

from flask_mail import Message, Mail

from bookcrossing.models.models import(User,
                                       Book,
                                       BookRequest,
                                       db)

mail = Mail()


def generate_uuid() -> str:
    return str(uuid.uuid4())


def create_book_request(book_id: int, requester_id: int) -> bool:
    requester = User.query.get(requester_id)
    if requester.points < requester.limit:
        requester.points += 1

        db.session.add(requester)
        db.session.commit()

        book = Book.query.get(book_id)

        book_request = BookRequest(book_id, requester_id, book.user_id)
        #book_request.id = generate_uuid()

        db.session.add(book_request)
        db.session.commit()

        return True
    else:
        return False


def send_email_notification(recipient: str, title: str, msg_body: str) -> bool:
    msg = Message(title,
                  sender='dmytro.test.test@gmail.com',
                  recipients=[recipient])
    msg.body = msg_body
    mail.send(msg)
    return True
