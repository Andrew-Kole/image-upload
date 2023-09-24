"""
Serializers for Picture API
"""
from rest_framework import serializers
from ..core.models import Picture


class PictureSerializer(serializers.ModelSerializer):
    """Serializer for pictures"""
    class Meta:
        model = Picture
        fields = ['id', 'title', 'link', 'expires_at']
        read_only_fields = ['id', 'created_at']

