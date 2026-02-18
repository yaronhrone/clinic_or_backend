from django.urls import path

from .views import Registerviews

urlpatterns = [
    path('register/', Registerviews.as_view(), name='user-register'),
]