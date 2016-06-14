import config

from flask import Flask
from flask_log import Logging
from flask_restful import Api
from flask_bootstrap import Bootstrap


from bookcrossing.resources import (resources,
                                    book_request_resources)
from bookcrossing.models.models import (login_manager,
                                        db)
from bookcrossing.mail import mail
from bookcrossing.resources.resources_user import (hello,
                                                   registration,
                                                   login,
                                                   logout)

app = Flask(__name__,
            root_path=config.root_path,
            template_folder=config.template_folder,
            static_folder=config.static_folder)

app.config.from_object(config.DevelopmentConfig)

api = Api(app, prefix='/bookcrossing/v1')

flask_log = Logging(app)

db.init_app(app)

with app.app_context():
    db.create_all()

# engine = config.DevelopmentConfig.create_psql_engine()

#  Register your urls here
api.add_resource(resources.Index, '/', '/index')
api.add_resource(book_request_resources.BookRequestResource,
                 '/book-request/<int:book_id>/<int:requester_id>',
                 '/book-request/<int:request_id>')

bootstrap = Bootstrap()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

bootstrap.init_app(app)
mail.init_app(app)
login_manager.init_app(app)

app.add_url_rule('/', 'hello', hello)
app.add_url_rule('/registration', 'registration', registration, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout)
