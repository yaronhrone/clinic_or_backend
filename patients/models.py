from django.db import models
from django.conf import settings

class PatientProfile(models.Model):
    """Model representing a patient profile."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL
                                , on_delete=models.CASCADE
                                , related_name='patient_profile')

    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.user.email