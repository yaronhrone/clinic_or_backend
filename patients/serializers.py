from rest_framework import serializers


from patients.models import PatientProfile

class PatientProfileSerializer(serializers.ModelSerializer):
    """Serializer for the PatientProfile model."""

    class Meta:
        model = PatientProfile
        fields = ['phone_number', 'address', 'gender', 'date_of_birth']

        def validate(self,attrs):
            """Validate the patient profile data"""
            user= self.context['request'].user
            if PatientProfile.objects.filter(user=user).exists():
                raise serializers.ValidationError(
                    "Patient profile already exists for this user."
                    )
            return attrs

    def create(self, validated_data):
        """Create a new patient profile."""
        user = self.context['request'].user
        return PatientProfile.objects.create(user=user, **validated_data)