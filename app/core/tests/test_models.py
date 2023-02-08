from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTest(TestCase):
    """Test User Model"""

    def test_create_user_with_email(self):
        """Test the creation of a basic user with an email and password"""
        test_email = "test@example.com"
        test_password = "test123"
        user = get_user_model().objects.create_user(email = test_email, password = test_password)

        self.assertEqual(user.email, test_email)
        self.assertTrue(user.check_password(test_password))
