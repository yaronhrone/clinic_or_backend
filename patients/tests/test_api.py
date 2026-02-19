from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from patients.models import PatientProfile

User = get_user_model()


class PatientAPITestCase(APITestCase):
    """Test case for patient API endpoints."""

    def setUp(self):
        """Set up the test case."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User"
        )
        login_url = reverse('token_obtain_pair')

        response = self.client.post(login_url,{
            'email': 'test@example.com',
            'password': 'testpassword'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_create_patient_profile(self):
        """Test creating a new patient profile."""
        url = reverse('patient-create')

        payload = {
           "phone_number": "1234567890",
            "address": "123 Test Street",
            "gender": "M",
            "date_of_birth": "1990-01-01"
        }
        response = self.client.post(url,payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PatientProfile.objects.count(), 1)
        self.assertEqual(PatientProfile.objects.first().user.email, "test@example.com")
