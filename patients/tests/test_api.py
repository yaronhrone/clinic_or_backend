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

    def test_get_patient_profile(self):
        """Test retrieving the patient profile."""
        patient = PatientProfile.objects.create(
            user=self.user,
            phone_number="1234567890",
            address="123 Test Street",
            gender="M",
            date_of_birth="1990-01-01"
        )
        url = reverse('patient-me')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], patient.phone_number)

    def test_update_patient_profile(self):
        """Test updating the patient profile."""
        patient = PatientProfile.objects.create(
            user=self.user,
            phone_number="1234567890",
            address="123 Test Street",
            gender="M",
            date_of_birth="1990-01-01"
        )
        url = reverse('patient-me')
        payload = {
            "phone_number": "0987654321",
            "address": "456 Test Avenue",
            "gender": "F",
            "date_of_birth": "1991-01-01"
        }
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        patient.refresh_from_db()
        self.assertEqual(patient.phone_number, "0987654321")
        self.assertEqual(patient.address, "456 Test Avenue")
        self.assertEqual(patient.gender, "F")


    def test_get_profile_returns_404_if_not_exists(self):
        """Test that getting a profile that doesn't exist returns 404."""
        url = reverse('patient-me')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

