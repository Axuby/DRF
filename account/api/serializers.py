
from pyexpat import model
import re
from django.contrib.auth.models import User
# from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class ManageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", ]


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username',  'email', 'password', 'password2')
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    def validate(self, attrs):
        if not attrs.get('password') == attrs.get('password2'):
            raise serializers.ValidationError("Passwords doesn't match!")
        return attrs

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Email already in use")
        return lower_email

    # def save(self, **kwargs):
    #     password = self.validated_data.get("password")
    #     password2 = self.validated_data.get("password2")
    #     if password != password2:
    #         raise serializers.ValidationError("Password dont match!")\
        # if User.objects.filter(email=self.validated_data['email']).exists():
        #     raise serializers.ValidationError("email already in use")

        account = User.objects.create(
            username=self.validated_data['username'], email=self.validated_data['email'])
    #     return super().save(**kwargs)
