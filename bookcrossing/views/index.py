from flask import render_template, make_response
from flask_restful import Resource
import logging
import logging.config
from bookcrossing.config import LOGGING

logging.config.dictConfig(LOGGING)


class Index(Resource):
    def __init__(self):
        self.headers = {'Content-Type': 'text/html'}

    def get(self):
        logging.debug('Index resource')
        return make_response(render_template('index.html'), 200, self.headers)
