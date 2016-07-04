import sys
import os

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             '../..'))

from flask_testing import TestCase
from flask import Flask

from bookcrossing import db
from bookcrossing.config import TestingConfig
from bookcrossing.models.user import UserModel
from flask_fixtures import FixturesMixin


class TestDataBase(TestCase, FixturesMixin):
    fixtures = ['users.json']

    def create_app(self):
        app = Flask(__name__)
        app.config.from_object(TestingConfig)
        db.init_app(app)
        with app.app_context():
            db.create_all()
        return app

    # def setUp(self):
    #     test_user_1 = UserModel(login='MayerLogin',
    #                             password='Mayerpassword',
    #                             email='mayer@gmail.com',
    #                             first_name='Mayer',
    #                             last_name='Hawthorne',
    #                             office='Dnepr_office',
    #                             phone_number='12345678900')
    #     test_user_1.id = 11111
    #
    #     db.session.add(test_user_1)
    #     db.session.commit()

    def test_user(self):
        user_1 = UserModel.query.get(11111)

        self.assertIn(user_1, db.session)
        self.assertEqual(user_1.login, 'MayerLogin')
        self.assertEqual(user_1.email, 'mayer@gmail.com')
        self.assertEqual(user_1.first_name, 'Mayer')
        self.assertEqual(user_1.last_name, 'Hawthorne')
        self.assertEqual(user_1.office, 'Dnepr_office')
        self.assertEqual(user_1.phone_number, '12345678900')

    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()

if __name__ == '__main__':
    import unittest
    unittest.main()
