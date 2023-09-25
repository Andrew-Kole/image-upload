"""
Views for the Picture API
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from . import serializers
from core.models import Picture # noqa


class PictureViewSet(viewsets.ModelViewSet):
    """View for manage Picture API"""
    serializer_class = serializers.PictureDetailSerializer
    queryset = Picture.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """retrieves images list for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """returns serializer class for request"""
        if self.action == 'list':
            return serializers.PictureSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """creates new picture"""
        serializer.save(user=self.request.user)
