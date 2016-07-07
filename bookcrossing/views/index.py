import logging.config

from flask import render_template

from bookcrossing.config import LOGGING
from bookcrossing.views.base_view import BaseMethodView

logging.config.dictConfig(LOGGING)


class Index(BaseMethodView):

    def get(self):
        return render_template('index.html')
