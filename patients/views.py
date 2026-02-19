from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveUpdateAPIView

from .models import PatientProfile
from .serializers import PatientProfileSerializer

class PatientProfileCreateView(APIView):
    """View for creating and retrieving patient profiles."""

    permission_classes = [IsAuthenticated]


    def post(self, request):
        """Create a new patient profile."""
        serializer = PatientProfileSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientProfileMeView(RetrieveUpdateAPIView):
    """View for retrieving and updating patient profiles."""
    permission_classes = [IsAuthenticated]
    serializer_class = PatientProfileSerializer

    def get_object(self):
        """Retrieve the patient's profile."""
        try:
            return PatientProfile.objects.get(user=self.request.user)
        except PatientProfile.DoesNotExist:
            raise NotFound("Patient profile not found for this user.")