from django.urls import path

from .views import PatientProfileCreateView , PatientProfileMeView

urlpatterns = [
    path("", PatientProfileCreateView.as_view(), name="patient-create"),
    path("me/", PatientProfileMeView.as_view(), name="patient-me"),
]