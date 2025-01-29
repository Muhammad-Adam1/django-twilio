from rest_framework import serializers
from .models import TwilioCredentials

class TwilioCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwilioCredentials
        fields = ['account_sid', 'auth_token', 'phone_number']