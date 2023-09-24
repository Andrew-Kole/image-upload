"""
Views for user API
"""

from rest_framework import (
    generics,
    authentication,
    permissions
)
from .serializers import (
    UserSerializer,
    AuthTokenSerializer,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(generics.CreateAPIView):
    """represents creating a new user"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """represents creation a token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """represents authenticated user management"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """retrieves and returns authenticated user"""
        return self.request.user
