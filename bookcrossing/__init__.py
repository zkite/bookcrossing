import config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_log import Logging
from flask_restful import Api
from bookcrossing.resources import resources
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,
            root_path=config.root_path,
            template_folder=config.template_folder,
            static_folder=config.static_folder)

app.config.from_object(config.DevelopmentConfig)

api = Api(app, prefix='/bookcrossing/v1')

db = SQLAlchemy(app)

db.init_app(app)

flask_log = Logging(app)

#engine = config.ProductionConfig.create_engine()

#  Register your urls here
api.add_resource(resources.Index, '/', '/index')
api.add_resource(resources.Home, '/home')
