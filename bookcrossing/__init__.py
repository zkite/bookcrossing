import os

<<<<<<< HEAD
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
=======
from flask import Flask
>>>>>>> master
from flask_restful import Api
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap
from bookcrossing.config import runtime_config

<<<<<<< HEAD

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

=======
from bookcrossing.resources import (book_request_resources,
                                    show_user_profile)
from bookcrossing.models.models import (login_manager,
                                        db)
from bookcrossing.mail import mail
from bookcrossing.resources.resources_user import (hello,
                                                   registration,
                                                   login,
                                                   logout)

from bookcrossing.resources.edit_user_profile import (edit_user,
                                                      update_user)

import bookcrossing.resources.books as books

# app = Flask(__name__,
#             root_path=config.root_path,
#             template_folder=config.template_folder,
#             static_folder=config.static_folder)
>>>>>>> master

# dev, prod, test
APP_STATUS = 'dev'

mail = Mail()

<<<<<<< HEAD
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
=======
# engine = config.DevelopmentConfig.create_psql_engine()

bootstrap = Bootstrap()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

db.init_app(app)
with app.app_context():
    db.create_all()

bootstrap.init_app(app)

mail.init_app(app)
>>>>>>> master

login_manager.init_app(app)

<<<<<<< HEAD
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
=======
#  Register your urls here
app.add_url_rule('/', 'hello', hello)
>>>>>>> master
app.add_url_rule('/registration', 'registration', registration, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout)

<<<<<<< HEAD
app.add_url_rule('/user_profile', 'user_profile', user_profile)
app.add_url_rule('/edit_profile', 'edit_profile', edit_profile, methods=['GET', 'POST'])

=======
# books CRUD
app.add_url_rule('/books', 'books.index', books.index)
app.add_url_rule('/books/new', 'books.new', books.new, methods=['GET', 'POST'])
app.add_url_rule('/books/<int:book_id>', 'books.show', books.show)
app.add_url_rule('/books/<int:book_id>/edit', 'books.edit', books.edit, methods=['GET'])
app.add_url_rule('/books/<int:book_id>/edit', 'books.update', books.update, methods=['POST'])

app.add_url_rule('/profile/edit', 'user.edit', edit_user, methods=['GET'])
app.add_url_rule('/profile/edit', 'user.update', update_user, methods=['POST'])

#  Register your REST urls here
api.add_resource(book_request_resources.BookRequestResource,
                 '/book-request/<int:book_id>',  # method == 'POST'
                 '/book-request/<int:request_id>',  # method == 'DELETE'
                 '/user-book-requests')  # method == 'GET'
api.add_resource(show_user_profile.ShowProfile,
                 '/show-user-profile')  # method == 'GET'
>>>>>>> master
