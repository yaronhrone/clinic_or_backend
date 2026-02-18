from django.test import TestCase
from django.contrib.auth import get_user_model


from users.models import User

class UserAPITestCase(TestCase):
    """Test case for user API endpoints."""

    def test_create_user(self):
        """Test creating a new user."""
        user = User.objects.create_user(
            email = 'test@example.com',
            password = 'testpassword',
            first_name = 'Test',
            last_name = 'User'
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpassword"))
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="",
                password="123456",
                first_name="Test",
                last_name="User",
            )

