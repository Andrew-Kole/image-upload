"""
Serializers for Picture API
"""
from rest_framework import serializers

from core.models import Picture # noqa


class PictureSerializer(serializers.ModelSerializer):
    """Serializer for pictures"""
    class Meta:
        model = Picture
        fields = ['id', 'title', 'link', 'expires_at']
        read_only_fields = ['id', 'created_at']


class PictureDetailSerializer(PictureSerializer):
    """Serializer for picture details view."""
    class Meta(PictureSerializer.Meta):
        fields = PictureSerializer.Meta.fields + ['description']
