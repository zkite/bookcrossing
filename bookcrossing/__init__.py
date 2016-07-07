import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from bookcrossing.config import runtime_config


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# dev, prod, test
APP_STATUS = 'dev'


app = Flask(__name__)
app.config.from_object(runtime_config(APP_STATUS))

bootstrap = Bootstrap(app)

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

mail = Mail(app)

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = '/login/'

from bookcrossing.views.index import Index
from bookcrossing.views.search.book_search import BookSearchView
from bookcrossing.views.request_history.request_history import RequestHistoryView
from bookcrossing.views.books.book import (
    BooksView,
    BookProfileView
)
from bookcrossing.views.request.request import (
    RequestView,
    DeclineRequestView
)
from bookcrossing.views.user.user import (
    RegistrationView,
    LoginView,
    LogoutView,
    UsersListView,
    UserProfileView,
    EditUserProfileView,
    RestorePasswordView
)
from bookcrossing.views.error_handlers import (
    page_not_found,
    forbidden,
    gone,
    internal_server_error,
)

user_reg = RegistrationView.as_view('user_reg')
app.add_url_rule('/registration/',  view_func=user_reg, methods=['GET', 'POST'])

user_login = LoginView.as_view('user_login')
app.add_url_rule('/login/',  view_func=user_login, methods=['GET', 'POST'])

user_logout = LogoutView.as_view('user_logout')
app.add_url_rule('/logout/',  view_func=user_logout, methods=['GET'])

users_list = UsersListView.as_view('users_list')
app.add_url_rule('/users/',  view_func=users_list, methods=['GET'])

user_profile = UserProfileView.as_view('user_info')
app.add_url_rule('/profile/', view_func=user_profile, methods=['GET'])
app.add_url_rule('/profile/<int:user_id>', view_func=user_profile, methods=['GET'])

edit_profile = EditUserProfileView.as_view('us_profile')
app.add_url_rule('/edit/',  view_func=edit_profile, methods=['GET', 'POST'])

restore_password = RestorePasswordView.as_view('restore_password')
app.add_url_rule('/restore/',  view_func=restore_password, methods=['GET', 'POST'])

index_view = Index.as_view('index')
app.add_url_rule('/', view_func=index_view, methods=['GET'])

book_view = BooksView.as_view('book_view')
app.add_url_rule('/books', view_func=book_view, methods=['POST', 'GET', 'PUT', 'DELETE'])

book_profile_view = BookProfileView.as_view('book_profile_view')
app.add_url_rule('/books/<int:book_id>', view_func=book_profile_view, methods=['GET'])

search_view = BookSearchView.as_view('search_view')
app.add_url_rule('/search', view_func=search_view, methods=['POST', 'GET'])

request_view = RequestView.as_view('request')
app.add_url_rule(rule='/requests/<int:request_id>', view_func=request_view,
                 methods=['PUT', 'DELETE'])
app.add_url_rule(rule='/books/<int:book_id>/requests', view_func=request_view,
                 methods=['POST'])
app.add_url_rule(rule='/requests', view_func=request_view,
                 methods=['GET'])

decline_request_view = DeclineRequestView.as_view('decline_request')
app.add_url_rule(rule='/requests/decline/<int:request_id>', view_func=decline_request_view,
                 methods=['POST'])

req_history_view = RequestHistoryView.as_view("req_history_view")
app.add_url_rule(rule="/requests/history", view_func=req_history_view, methods=['GET'])


app.register_error_handler(404, page_not_found)
app.register_error_handler(403, forbidden)
app.register_error_handler(410, gone)
app.register_error_handler(500, internal_server_error)
