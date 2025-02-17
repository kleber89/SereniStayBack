import unittest
from app.models.user import Create_User, User, verify_password, Name
from pydantic import ValidationError
from passlib.context import CryptContext

class TestUserModels(unittest.TestCase):

    def test_valid_name(self):
        name = Name(first_name="John", second_name="Doe", last_name="Smith")
        self.assertEqual(name.first_name, "John")
        self.assertEqual(name.last_name, "Smith")
        self.assertEqual(name.second_name, "Doe")

    def test_invalid_email(self):
        with self.assertRaises(ValidationError):
            Create_User(name=Name(first_name="John", last_name="Smith"),
                        email="invalid-email", password="password123")

    def test_valid_password_hashing(self):
        user = Create_User(name=Name(first_name="John", last_name="Smith"),
                           email="john.smith@gmail.com", password="password123")
        self.assertTrue(verify_password("password123", user.password))

    def test_invalid_password(self):
        user = Create_User(name=Name(first_name="John", last_name="Smith"),
                           email="john.smith@gmail.com", password="password123")
        self.assertFalse(verify_password("wrongpassword", user.password))

    def test_email_domain_validation(self):
        with self.assertRaises(ValueError):
            User(name=Name(first_name="John", last_name="Smith"),
                 email="john.doe@yahoo.com", hashed_password="hashedpassword123")

    def test_valid_phone_number(self):
        user = Create_User(name=Name(first_name="John", last_name="Smith"),
                           email="john.smith@gmail.com", num_phone="1234567890", password="password123")
        self.assertEqual(user.num_phone, "1234567890")

    def test_invalid_phone_number(self):
        with self.assertRaises(ValidationError):
            Create_User(name=Name(first_name="John", last_name="Smith"),
                        email="john.smith@gmail.com", num_phone="12345678901", password="password123")

if __name__ == '__main__':
    unittest.main()
