"""
Views for the Picture API
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from . import serializers
from ..core.models import Picture


class PictureViewSet(viewsets.ModelViewSet):
    """View for manage Picture API"""
    serializer_class = serializers.PictureSerializer
    queryset = Picture.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """retrieves images list for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')
