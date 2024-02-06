from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerializer
from .models import User


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by("-date_joined")
