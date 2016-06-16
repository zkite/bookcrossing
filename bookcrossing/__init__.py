import os

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_restful import Api
from flask_mail import Mail, Message
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


from bookcrossing.resources.index import Index
# from bookcrossing.resources.login import Login
# from bookcrossing.resources.register import Register
# from bookcrossing.resources.logout import Logout
from bookcrossing.resources.search import Search
from bookcrossing.resources.book import BooksResource, BookProfileResource
from bookcrossing.resources.book import BooksResource, BookProfileResource
from bookcrossing.resources.requests import RequestsResource, RequestProfileResource


api.add_resource(Index, '/')
# api.add_resource(Login, '/login')
# api.add_resource(Register, '/register')
# api.add_resource(Logout, '/logout')
api.add_resource(Search, '/search')
api.add_resource(BooksResource, '/books')
api.add_resource(BookProfileResource, '/books/<int:id>')
api.add_resource(RequestsResource, '/requests', '/requset/<int:req_id>', '/books/<int:book_id>/requests')
api.add_resource(RequestProfileResource, '/books/<int:book_id>/requests/<int:req_id>')

# Views(controllers) for user_resources ----------------
from bookcrossing.resources.user_resources import (index,
                                                   users,
                                                   registration,
                                                   login,
                                                   logout,
                                                   user_profile,
                                                   edit_profile)

# app.add_url_rule('/', 'hello', index)
# app.add_url_rule('/users', 'users', users)
app.add_url_rule('/registration', 'registration', registration, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout)

app.add_url_rule('/user_profile', 'user_profile', user_profile)
app.add_url_rule('/edit_profile', 'edit_profile', edit_profile, methods=['GET', 'POST'])

