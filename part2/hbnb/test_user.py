#!/usr/bin/env python3
import unittest

from app.models.user import User


class TestUser(unittest.TestCase):
    def test_create_valid_user(self):
        u = User(first_name="Test", last_name="User", email="test@hbnb.com")
        self.assertEqual(u.first_name, "Test")
        self.assertEqual(u.last_name, "User")
        self.assertEqual(u.email, "test@hbnb.com")
        self.assertFalse(u.is_admin)

    def test_to_dict_keys(self):
        u = User(first_name="A", last_name="B", email="a@b.com", is_admin=True)
        d = u.to_dict()
        self.assertIn("id", d)
        self.assertIn("first_name", d)
        self.assertIn("last_name", d)
        self.assertIn("email", d)
        self.assertIn("is_admin", d)

    def test_invalid_email_should_fail(self):
        with self.assertRaises(Exception):
            User(first_name="A", last_name="B", email="bademail")

    def test_empty_first_or_last_should_fail(self):
        with self.assertRaises(Exception):
            User(first_name="", last_name="B", email="a@b.com")
        with self.assertRaises(Exception):
            User(first_name="A", last_name="", email="a@b.com")


if __name__ == "__main__":
    unittest.main(verbosity=2)
