import config

from flask import Flask
from flask_log import Logging
from flask_restful import Api

from bookcrossing.models.models import db
from bookcrossing.resources import resources

app = Flask(__name__,
            root_path=config.root_path,
            template_folder=config.template_folder,
            static_folder=config.static_folder)

app.config.from_object(config.ProductionConfig)

api = Api(app, prefix='/bookcrossing/v1')

flask_log = Logging(app)

db.init_app(app)

with app.app_context():
    db.create_all()

engine = config.ProductionConfig.create_psql_engine()

#  Register your urls here
api.add_resource(resources.Index, '/', '/index')
