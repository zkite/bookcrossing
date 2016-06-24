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
login_manager.login_view = 'login'

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


# Views(controllers) for user_resources ----------------

from bookcrossing.views.registration.registration import RegistrationView
user_reg = RegistrationView.as_view('user_reg')
app.add_url_rule('/registration/',  view_func=user_reg, methods=['GET'])
app.add_url_rule('/registration/',  view_func=user_reg, methods=['POST'])

from bookcrossing.views.login.login import LoginView
user_login = LoginView.as_view('user_login')
app.add_url_rule('/login/',  view_func=user_login, methods=['GET'])
app.add_url_rule('/login/',  view_func=user_login, methods=['POST'])

from bookcrossing.views.logout.logout import LogoutView
user_logout = LogoutView.as_view('user_logout')
app.add_url_rule('/logout/',  view_func=user_logout, methods=['GET'])

from bookcrossing.views.user_profile.user_profile import UserProfileView
us_profile = UserProfileView.as_view('us_profile')
app.add_url_rule('/user_profile/',  view_func=us_profile, methods=['GET'])
app.add_url_rule('/edit_profile/',  view_func=us_profile, methods=['POST'])

from bookcrossing.views.users_list.users_list import UsersListView
users_list = UsersListView.as_view('users_list')
app.add_url_rule('/users_list/',  view_func=users_list, methods=['GET'])
