import requests
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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
    phone = serializers.CharField(
        max_length=9,
        required=True,
        style={'input_type': 'text'}
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
        fields = ["username", "password", "password_confirm", "phone"]

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        phone = data.get('phone')

        if password and password_confirm and password != password_confirm:
            raise serializers.ValidationError("Пароллар бир хил эмас!")

        return data

    def create(self, validated_data):
        username = validated_data.get("username")
        password = validated_data.get("password")
        phone = validated_data.get("phone")
        print(phone)
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Бундай фойдаланувчи аллақачон мавжуд.")

        user = User(username=username, phone=phone)

        url = 'https://notify.eskiz.uz/api/message/sms/send'
        data = {
            'mobile_phone': f'998{phone}',
            'message': f"Tabriklayman!\n\nSiz Geeks platformasida {username} logini bilan ro'yhatdan o'tdingiz.\n\nAgarda mana shunday ishlarni qila olishni xoxlasangiz, hoziroq Backend kursiga yoziling... ",
            'from': '4546',
        }
        headers = {
            'Authorization': f'Bearer {TOKEN}',
        }

        response = requests.post(url, headers=headers, data=data)

        user.set_password(password)
        user.save()

        return user

