from unittest import TestCase
from pydantic import ValidationError
from app.models.user import Name, Create_User, User, verify_password
from passlib.context import CryptContext
from app.models.user import pwd_context

class TestUserModel(TestCase):

    def test_user_creation(self):
        name = Name(first_name="Test", last_name="User")
        user = Create_User(name=name, email="test@gmail.com", num_phone="1234567890", password="password123")
        self.assertEqual(user.name.first_name, "Test")
        self.assertEqual(user.email, "test@gmail.com")
        self.assertEqual(user.num_phone, "1234567890")
        self.assertIsNotNone(user.password)

    def test_user_invalid_num_phone(self):
        name = Name(first_name="Test", last_name="User")
        with self.assertRaises(ValidationError) as context:
            Create_User(name=name, email="test@gmail.com", num_phone="123456789", password="password123")
        self.assertIn("string_pattern_mismatch", str(context.exception))

        with self.assertRaises(ValidationError) as context:
            Create_User(name=name, email="test@gmail.com", num_phone="12345678901", password="password123")
        self.assertIn("string_pattern_mismatch", str(context.exception))

    def test_verify_password(self):
        password = "password123"
        hashed_password = pwd_context.hash(password)
        self.assertTrue(verify_password(password, hashed_password))
        self.assertFalse(verify_password("wrong_password", hashed_password))

    def test_verify_email(self):
        email = "sebas@gmail.com"
        
        # Crear un usuario con un correo electrónico válido
        user = Create_User(name=Name(first_name="Test", last_name="User"), 
                    email=email, 
                    num_phone="1234567890", 
                    password="password123")
        
        #verificar que el correo se alla agrgado correctamente
        self.assertEqual(user.email, email)
        print(user.password)
