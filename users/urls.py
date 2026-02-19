from django.urls import path

from django.urls import include

from .views import Registerviews
from .views import UserView

urlpatterns = [
    path('register/', Registerviews.as_view(), name='user-register'),
    path("me/", UserView.as_view(), name="user-me"),
    path("api/patients/", include("patients.urls")),
]