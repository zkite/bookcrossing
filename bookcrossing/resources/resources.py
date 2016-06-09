from flask_restful import Resource
from flask import make_response, render_template
from bookcrossing.models.models import User, db


# This is just example GET, POST methods working with render_template
class Index(Resource):

    def get(self):
        user_1 = User.query.first()
        return [user_1.login]

    def post(self):
        test_user = User('logisefnsef', 'passsefwoesfserd', 'ussefesefs_email', 'first_name', 'last_name', 'office', 'phone_numbe')
        db.session.add(test_user)
        db.session.commit()
        return make_response(render_template('index.html'), 200)


    def delete(self):
        test_user = User.query.all()[0]
        db.session.delete(test_user)
        db.session.commit()
        return ['Hello delete meth']
