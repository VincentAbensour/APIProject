from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminTest(TestCase):
    """Test Django Admin View"""
    def setUp(self):
        self.client = Client()
        superuser = get_user_model().objects.create_superuser(
            email = "admin@example.com",
            password = "admintest123",
            firstname = "admintestfirst",
            lastname = "admintestlast"
        )
        self.client.force_login(self.superuser)
        user = get_user_model().objects.create_user(
            email = "test@example.com",
            password = "test123",
            firstname = "testfirst",
            lastname = "testlast")

    def account_admin_view(self):
        url = reverse('admin:core_account_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def create_user_page(self):
        url = reverse('admin:core_account_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 220)