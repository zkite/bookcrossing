from bookcrossing import login_manager, app
from bookcrossing.models.user import UserModel
from flask_login import current_user
from flask import g


@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
