import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from bookcrossing.config import runtime_config


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# dev, prod, test
APP_STATUS = 'dev'

mail = Mail()

app = Flask(__name__)
app.config.from_object(runtime_config(APP_STATUS))

bootstrap = Bootstrap()
bootstrap.init_app(app)

api = Api(app)
db = SQLAlchemy(app)
mail.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = '/login/'

from bookcrossing.views.index import Index
from bookcrossing.views.search import Search
from bookcrossing.views.books.book import BooksResource, BookProfileResource
from bookcrossing.views.books.book import BooksResource, BookProfileResource
from bookcrossing.views.requests import RequestsResource, RequestProfileResource

api.add_resource(Index, '/')
api.add_resource(Search, '/search')
api.add_resource(BooksResource, '/books')
api.add_resource(BookProfileResource, '/books/<int:id>')
api.add_resource(RequestsResource, '/requests', '/requset/<int:req_id>', '/books/<int:book_id>/requests')
api.add_resource(RequestProfileResource, '/books/<int:book_id>/requests/<int:req_id>')


# Views(controllers) for user ----------------

from bookcrossing.views.user.user import (
    RegistrationView,
    LoginView,
    LogoutView,
    UsersListView,
    UserProfileView,
    EditUserProfileView
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
