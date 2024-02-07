import requests
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model

from my import TOKEN

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        max_length=20,
        style={'input_type': 'password'}
    )

    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    username = serializers.CharField(
        validators=[UnicodeUsernameValidator()],
        min_length=3,
        max_length=20,
        required=True
    )

    class Meta:
        model = User
        fields = ["username", "password", "password_confirm"]

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise serializers.ValidationError("The password and the repeated password are not the same!")

        return data

    def create(self, validated_data):
        username = validated_data.get("username")
        password = validated_data.get("password")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User already exists.")

        user = User(username=username)

        user.set_password(password)
        user.save()


        return user
