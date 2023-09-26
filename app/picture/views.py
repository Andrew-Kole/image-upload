"""
Views for the Picture API
"""
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from . import serializers
from core.models import Picture # noqa
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from .image_resizer import generate_thumbnail


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
        elif self.action == 'upload_image':
            return serializers.PictureImageSerializer
        elif self.action == 'thumbnail-small':
            return serializers.PictureThumbnailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """creates new picture"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload image"""
        picture = self.get_object()
        serializer = self.get_serializer(picture, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=True, url_path='thumbnail-small')
    def get_thumbnail_small(self, request, pk=None):
        picture = self.get_object()
        thumbnail = generate_thumbnail(picture.image.path, 200)
        res = HttpResponse(thumbnail, content_type='image/jpeg')

        return res
