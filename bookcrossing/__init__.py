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

db.init_app(app)
with app.app_context():
    db.create_all()

mail.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from bookcrossing.views.index import Index
# from bookcrossing.views.login import Login
# from bookcrossing.views.register import Register
# from bookcrossing.views.logout import Logout
from bookcrossing.views.search import Search
from bookcrossing.views.books.book import BooksResource, BookProfileResource
from bookcrossing.views.books.book import BooksResource, BookProfileResource
from bookcrossing.views.request.request import RequestView

api.add_resource(Index, '/')
# api.add_resource(Login, '/login')
# api.add_resource(Register, '/register')
# api.add_resource(Logout, '/logout')
api.add_resource(Search, '/search')
api.add_resource(BooksResource, '/books')
api.add_resource(BookProfileResource, '/books/<int:id>')

# Views(controllers) for user_resources ----------------
from bookcrossing.views.user_resources import (index,
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


request_view = RequestView.as_view('request')
app.add_url_rule(rule='/request/req-id/<int:request_id>', view_func=request_view,
                 methods=['GET', 'PUT', 'DELETE'])
app.add_url_rule(rule='/request/book-id/<int:book_id>', view_func=request_view,
                 methods=['POST'])
