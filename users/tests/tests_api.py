
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model



from rest_framework.test import APIClient


User = get_user_model()
class UserRegistrationAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user_success(self):
            """Test registering a new user via the API."""

            url = reverse('user-register')
            data = {
                'email': 'test@example.com',
                'password': 'testpassword',
                'first_name': 'Test',
                'last_name': 'User'
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, 201)
            self.assertEqual(User.objects.count(), 1)

            user = User.objects.first()
            self.assertEqual(user.email, "test@example.com")
            self.assertTrue(user.check_password("testpassword"))
            self.assertEqual(user.first_name, "Test")
            self.assertEqual(user.last_name, "User")
            self.assertNotIn('password', response.data)

    # def test_register_user_without_email(self):
    #     """Test registering a user without an email raises an error."""
    #     url = reverse('user-register')
    #     data = {
    #         'email': '',
    #         'password': 'testpassword',
    #         'first_name': 'Test',
    #         'last_name': 'User'
    #     }
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, 400)