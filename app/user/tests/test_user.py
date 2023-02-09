"""Tests for the user API"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status



CREATE_USER_URL = reverse('user:create_user')
TOKEN_URL = reverse('user:create_token')
ME_URL = reverse('user:myprofile')

def create_user_helper(**params):
    """ Create a new user """
    return get_user_model().objects.create_user(**params)

class PublicUserTests(TestCase):
    """ Test endpoints that don't need authentificaion """
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):

        user_logs = {
            "email" : "test@example.com",
            "password" : "test1234",
            "firstname" : "testfirst",
            "lastname" : "testlast",
        }

        response = self.client.post(CREATE_USER_URL, user_logs)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email = user_logs["email"])
        self.assertEqual(user.email, user_logs["email"])
        self.assertTrue(user.check_password(user_logs["password"]))
        self.assertNotIn('password', response.data)

    def test_check_user_email_unique(self):
        """Check if user's email already exists in the database"""
        user_logs = {
            "email" : "test@example.com",
            "password" : "test1234",
            "firstname" : "testfirst",
            "lastname" : "testlast"
        }

        create_user_helper(**user_logs)
        user = get_user_model().objects.get(email = user_logs["email"])
        response = self.client.post(CREATE_USER_URL, user_logs)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_user_password_length(self):
        """Check if user's password is less or equal than 8 characters"""
        user_logs = {
            "email" : "test@example.com",
            "password" : "test123",
            "firstname" : "testfirst",
            "lastname" : "testlast"
        }

        response = self.client.post(CREATE_USER_URL, user_logs)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(email = user_logs["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_token(self):
        """Test if actually Generate a token for authentification"""
        user_logs = {
            "email" : "test@example.com",
            "password" : "test1234",
            "firstname" : "testfirst",
            "lastname" : "testlast"
        }

        create_user_helper(**user_logs)

        user_logger = {
            'email' : user_logs['email'],
            'password' : user_logs['password'],
        }

        response = self.client.post(TOKEN_URL,user_logger)
        self.assertIn('token', response.data )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_bad_credentials(self):
        """Test if a token is still generated when bad credentials are used"""
        user_logs = {
            "email" : "test@example.com",
            "password" : "test1234",
            "firstname" : "testfirst",
            "lastname" : "testlast"
        }
        create_user_helper(**user_logs)

        user_logger = {
            'email' : 'bademail@test.test',
            'password' : user_logs['password'],
        }

        response = self.client.post(TOKEN_URL,user_logger)
        self.assertNotIn('token', response.data )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_blank_password(self):
        user_logs = {
            "email" : "test@example.com",
            "password" : "test1234",
            "firstname" : "testfirst",
            "lastname" : "testlast"
        }
        create_user_helper(**user_logs)
        user_logger = {
            'email' : 'test@example.com',
            'password' : '',
        }
        response = self.client.post(TOKEN_URL,user_logger)
        self.assertNotIn('token', response.data )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_mandatory_auth_profile(self):
        """"Test that authentification is needed to acces profil page"""

        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class AuthenticatedUserTests(TestCase):
    """ Test endpoints that require authentificaion """

    def setUp(self):
        self.user = create_user_helper(
            email = "test@example.com",
            password = "test1234",
            firstname = "testfirst",
            lastname = "testlast"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_reach_profile(self):
        """Test myprofile endpoint for looged user"""
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'email' : self.user.email,
            'firstname' : self.user.firstname,
            'lastname' : self.user.lastname,
        })

    def test_get_only_myprofile(self):
        """Test myprofile endpoint can't receive post request"""
        response = self.client.post(ME_URL,{})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_myprofile(self):
        """Test the update myprofile endpoint"""
        response = self.client.patch(ME_URL,{'firstname' : 'newfirstname'})
        self.user.refresh_from_db()
        self.assertEqual('newfirstname', self.user.firstname)
        self.assertEqual(response.status_code, status.HTTP_200_OK)





