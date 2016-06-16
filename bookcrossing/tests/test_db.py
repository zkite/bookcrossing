from flask_testing import TestCase
from flask import Flask

from bookcrossing import db
from myconfig import TestingConfig
from bookcrossing.models.models import User


class TestDataBase(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config.from_object(TestingConfig)

        db.init_app(app)
        with app.app_context():
            db.create_all()

        return app

    def setUp(self):
        test_user_1 = User('MayerLogin', 'Mayerpassword', 'mayer@gmail.com',
                           'Mayer', 'Hawthorne', 'Dnepr_office', '12345678900')

        test_user_2 = User('JakeLogin', 'Jakepassword', 'jake@gmail.com',
                           'Jake', 'Black', 'Lviv_office', '09876543211')

        db.session.add(test_user_1)
        db.session.add(test_user_2)
        db.session.commit()

    def test_users(self):
        user_1 = User.query.all()[0]
        user_2 = User.query.all()[1]

        self.assertNotEqual(user_1.id, user_2.id)
        self.assertIn(user_1, db.session)
        self.assertIn(user_2, db.session)
        self.assertEqual(user_1.login, 'MayerLogin')
        self.assertEqual(user_2.login, 'JakeLogin')
        self.assertEqual(user_1.email, 'mayer@gmail.com')
        self.assertEqual(user_2.email, 'jake@gmail.com')
        self.assertEqual(user_1.password, 'Mayerpassword')
        self.assertEqual(user_2.password, 'Jakepassword')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
