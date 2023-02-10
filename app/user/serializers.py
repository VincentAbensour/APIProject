""" Serializers For The User App"""

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from core.models import Account

class UserSerializer(serializers.ModelSerializer):
    """ Serializers For The User Object"""

    class Meta:
        model = Account
        fields = ["email","password","firstname","lastname"]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8 }}

    def create(self, validated_data):
        """ Create the user with encrypted password"""
        return Account.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update The user"""
        user = super().update(instance,validated_data)

        return user

class AuthTokenSerializer(serializers.Serializer):
    """ Serializers For The User Token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type':'password'}
    )

    def validate(self, data):
        """Validate and Authenticate the User"""
        email = data.get('email')
        password = data.get('password')
        user = authenticate(
            email = email,
            password = password)

        if not user:
            raise serializers.ValidationError('Bad Credentials, no account linked to those')

        data['user'] = user
        return data