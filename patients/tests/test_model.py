from django.test import TestCase
from django.contrib.auth import get_user_model

from patients.models import PatientProfile

User = get_user_model()

class PatientModelTestCase(TestCase):
    """Test case for the Patient model."""

    def test_create_patient(self):
        """Test creating a new patient."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User"
        )
        patient = PatientProfile.objects.create(
            user=user,
            phone_number="1234567890",
            address="123 Test Street",
            gender="M",
            date_of_birth="1990-01-01"
        )
        self.assertEqual(patient.user, user)
        self.assertEqual(patient.phone_number, "1234567890")
        self.assertEqual(patient.address, "123 Test Street")
        self.assertEqual(patient.gender, "M")
        self.assertEqual(patient.date_of_birth, "1990-01-01")