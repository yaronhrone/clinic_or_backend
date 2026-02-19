from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PatientProfileSerializer

class PatientProfileView(APIView):
    """View for creating and retrieving patient profiles."""
    permission_classes = [IsAuthenticated]

    # def get(self, request):
    #     """Retrieve the patient's profile."""
    #     patient_profile = request.user.patient_profile
    #     serializer = PatientSerializer(patient_profile)
    #     return Response(serializer.data)

    def post(self, request):
        """Create a new patient profile."""
        serializer = PatientProfileSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)