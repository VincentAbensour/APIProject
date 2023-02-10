from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Recipe

class ModelTest(TestCase):
    """Test Basic User"""

    def test_create_user_with_email(self):
        """Test the creation of a basic user with an email, firstname, lastname and password"""
        test_email = "test@example.com"
        test_password = "test123"
        test_firstname = "firsttest"
        test_lastname = "lasttest"
        user = get_user_model().objects.create_user(email = test_email,
                                                    password = test_password,
                                                    firstname = test_firstname,
                                                    lastname = test_lastname)
        self.assertEqual(user.email, test_email)
        self.assertEqual(user.firstname, test_firstname)
        self.assertEqual(user.lastname, test_lastname)
        self.assertTrue(user.check_password(test_password))

    def test_user_email(self):
        """Test if user's email is normalized"""

        emails = [
            ["test@ExamPle.com",
            "test@example.com"],
            [
            "Test@EXAMPLE.com",
            "Test@example.com"
            ],
            [
            "TEST@EXAMPLE.COM",
            "TEST@example.com"
            ]
        ]

        for email in emails:
            user = get_user_model().objects.create_user(email = email[0],
                                                    firstname = "testfirst",
                                                    lastname = "testlast")
            self.assertEqual(email[1], user.email)

    """Test For SuperUser"""

    def test_create_super_user(self):
        """Test the creation of a basic user"""
        user = get_user_model().objects.create_superuser(
            email = "test@example.com",
            password = "test123",
            firstname = "testfirst",
            lastname = "testlast"
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password("test123"))
        self.assertEqual("test@example.com", user.email)
        self.assertEqual(user.firstname, "testfirst")
        self.assertEqual(user.lastname, "testlast")

    def test_superuser_email(self):
        """Test if user's email is normalized"""

        emails = [
            ["test@ExamPle.com",
            "test@example.com"],
            [
            "Test@EXAMPLE.com",
            "Test@example.com"
            ],
            [
            "TEST@EXAMPLE.COM",
            "TEST@example.com"
            ]
        ]

        for email in emails:
            user = get_user_model().objects.create_superuser(email = email[0],
                                                    firstname = "testfirst",
                                                    lastname = "testlast",
                                                    password = "testpassword")
            self.assertEqual(email[1], user.email)

    def test_create_recipe(self):
        user = get_user_model().objects.create_user(
            email = "test@example.com",
            password = "test1234",
            firstname = "testfirst",
            lastname = "testlast"
        )

        recipe = Recipe.objects.create(
            user = user,
            title = 'testrecipe',
            time = 5,
            price = 5.50,
            description = 'test recipe description'
            )
        exists = Recipe.objects.filter(title = 'testrecipe', user = user).exists()
        self.assertTrue(exists)