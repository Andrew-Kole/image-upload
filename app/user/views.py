"""
Views for user API
"""

from rest_framework import generics
from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """represents creating a new user"""
    serializer_class = UserSerializer
