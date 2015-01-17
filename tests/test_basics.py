import unittest
from flask import current_app
from app import create_app, db


# this test is writing using the basic library form python
class BasicsTestCase(unittest.TestCase):

    # execute after each test
    def setUp(self):
        # creates my app, as it was been executed normally, like
        # so i have access to my app
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    # execute before each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
