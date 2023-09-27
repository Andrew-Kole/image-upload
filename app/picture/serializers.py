"""
Serializers for Picture API
"""
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from core.models import Picture # noqa


class PictureSerializer(serializers.ModelSerializer):
    """Serializer for pictures"""
    class Meta:
        model = Picture
        fields = ['id', 'title', 'created_at',
                  'expires_at']
        read_only_fields = ['id', 'created_at', 'expires_at']

    def create(self, validated_data):
        """creates, saves and returns a new Picture object"""
        validated_data['created_at'] = timezone.now()
        validated_data['expires_at'] = (validated_data['created_at'] +
                                        timedelta(seconds=13500)) # noqa
        picture = Picture(**validated_data)
        picture.save()

        return picture


class PictureDetailSerializer(PictureSerializer):
    """Serializer for picture details view."""
    class Meta(PictureSerializer.Meta):
        fields = PictureSerializer.Meta.fields + ['description']


class PictureImageSerializer(serializers.ModelSerializer):
    """Serializer for image upload"""
    class Meta:
        model = Picture
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}


class PictureOriginalImageSerializer(PictureSerializer):
    """Serializer for original image get"""
    image_data = serializers.ImageField()
