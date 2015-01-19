import unittest
from app.models import Users, Role, Permission, AnonymousUser


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = Users(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = Users(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = Users(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = Users(password='cat')
        u2 = Users(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_roles_and_permissions(self):
        Role.insert_roles()
        u = Users(email='john@example.com', password='cat')
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))