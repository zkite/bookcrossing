import uuid
import datetime

# from bookcrossing.mail.email import send_async_email
from bookcrossing.models.user import UserModel
from bookcrossing.models.requests import RequestModel
from bookcrossing.models.book import BookModel


def generate_uuid() -> str:
    return str(uuid.uuid4())


def create_book_request(book_id, requester, book_model, request_model, db):
    requester.points += 1
    book = book_model.query.get(book_id)
    request_object = request_model(book_id, requester.id, book.user_id)

    # if requester.points < requester.limit:
    if True:
        db.session.add(request_object)
        db.session.add(requester)
        db.session.commit()
        return request_object
    else:
        return False


# def create_book_request(book_id: int, requester_id: int, db) -> bool:
#     requester = UserModel.query.get(requester_id)
#
#     if not requester:
#         return False
#
#     # TODO POINTS
#     # if requester.points < requester.limit:
#     if True:
#         requester.points += 1
#         book = BookModel.query.get(book_id)
#         book_request = RequestModel(book_id, requester_id, book.user_id)
#
#         db.session.add(book_request)
#         db.session.add(requester)
#         db.session.commit()
#         return book_request
#
#     else:
#         return False


def update_request(request_id, db, request_model, book_model):
    print(request_id)
    book_request = request_model.query.get(request_id)
    print(book_request)

    if not book_request:
        return False

    book = book_model.query.get(book_request.book_id)
    # book.visible = False
    book_request.accept_date = datetime.datetime.now()

    # db.session.add(book)
    db.session.add(book_request)
    db.session.commit()
    return book_request


def remove_request(request_id: int, db) -> bool:
    book_request = RequestModel.query.get(request_id)

    if not book_request:
        return False

    book = BookModel.query.get(book_request.book_id)
    book.user_id = book_request.req_user_id
    book.visible = True

    owner = UserModel.query.get(book_request.owner_user_id)
    owner.points -= 1

    db.session.add(book)
    db.session.add(owner)
    db.session.delete(book_request)
    db.session.commit()
    return True


def send_notification_email_created_book_request(book_id: int, requester_id: int) -> bool:
    requester = UserModel.query.get(requester_id)
    book = BookModel.query.get(book_id)
    owner = UserModel.query.get(book.id)
    ''''
    send_async_email(requester.email,
                     'Book Request Created',
                     'email/request_created.html',
                     user=requester)
    send_async_email(owner.email,
                     'Book Request Created',
                     'email/request_created.html',
                     user=owner)
                     '''
    return True


# TODO Just use other names
def get_requested_book_requests(user_id: int) -> list:
    list_requested_book_requests = RequestModel.query.filter_by(owner_user_id=user_id).all()
    if list_requested_book_requests:
        return list_requested_book_requests
    else:
        return None


def get_sent_book_requests(user_id: int) -> list:
    list_sent_book_requests = RequestModel.query.filter_by(req_user_id=user_id).all()
    if list_sent_book_requests:
        return list_sent_book_requests
    else:
        return None


def get_requests_by_category(category, request_model, request_schema, book_model, user_object, user_model):
    requests = None
    requests = list()
    request_list = None
    if category == 'incoming':
        request_list = request_model.query.filter_by(owner_user_id=user_object.id).all()
    if category == 'outcoming':
        request_list = request_model.query.filter_by(req_user_id=user_object.id).all()

    for req in request_list:
        parsed_requests = request_schema().dump(req).data
        parsed_requests['title'] = book_model.query.get(req.book_id).title
        parsed_requests['request_date'] = req.request_date.strftime("%y-%m-%d-%H-%M")
        parsed_requests['requester'] = user_model.query.get(req.req_user_id).login
        parsed_requests['accepter'] = user_model.query.get(req.owner_user_id).login
        print(parsed_requests)
        requests.append(parsed_requests)

    return requests
