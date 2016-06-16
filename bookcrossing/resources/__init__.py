from bookcrossing import login_manager, current_user, g, app
from bookcrossing.models.user import UserModel


@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
