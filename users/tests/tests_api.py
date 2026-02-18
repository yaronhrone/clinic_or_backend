from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status

from rest_framework.test import APIClient ,APITestCase


User = get_user_model()
def create_user(**params):
  return User.objects.create_user(**params)
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

    def test_register_user_without_email(self):
        """Test registering a user without an email raises an error."""
        url = reverse('user-register')
        data = {
            'email': '',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        user_exists = (get_user_model()
                       .objects.filter(email=data['email']).exists())
        self.assertFalse(user_exists)
    def test_rgister_user_without_first_name(self):
        """Test registering a user without a first name raises an error."""
        url = reverse('user-register')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': '',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_the_password_too_short(self):
        """Test registering a user with an invalid password raises an error."""
        url = reverse('user-register')
        data = {
            'email': 'test@example.com',
            'password': 'te',
            'first_name': 'Test',
            'last_name': 'User',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

class UserLoginAPITestCase(TestCase):
    """Test case for user login API endpoint."""

    def test_user_can_login_and_get_token(self):
        """Test that a user can log in and receive a JWT token."""
        # Create a test user
        user = create_user(email="test@example.com", password="testpassword")
        url = reverse('token_obtain_pair')

        response = self.client.post(url, {
            'email': user.email,
            'password': 'testpassword'
        }, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class UserMeAPITest(APITestCase):
    """Test case for user profile API endpoint."""

    def test_get_user_me_requires_authentication(self):
        """Test that the /me/ endpoint requires authentication."""
        url = reverse('user-me')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, 401)

    def test_get_user_me_returns_user_info(self):
        """Test that the /me/ endpoint returns the authenticated user's info."""
        user = create_user(email="test@example.com", password="testpassword")

        login_url = reverse('token_obtain_pair')
        token_response = self.client.post(login_url, {
            'email': user.email,
            'password': 'testpassword'
        }, format='json')
        access_token = token_response.data['access']

        url = reverse('user-me')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], user.email)
