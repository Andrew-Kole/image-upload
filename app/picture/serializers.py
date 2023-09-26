"""
Serializers for Picture API
"""
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from core.models import Picture # noqa


class PictureSerializer(serializers.ModelSerializer):
    """Serializer for pictures"""
    seconds_to_expire = serializers.IntegerField(write_only=True)

    class Meta:
        model = Picture
        fields = ['id', 'title', 'created_at',
                  'expires_at', 'seconds_to_expire']
        read_only_fields = ['id', 'created_at', 'expires_at']

    def create(self, validated_data):
        """creates, saves and returns a new Picture object"""
        seconds_to_expire = validated_data.pop('seconds_to_expire', None)
        validated_data['created_at'] = timezone.now()
        if seconds_to_expire is not None:
            validated_data['expires_at'] = (validated_data['created_at'] +
                                            timedelta(seconds=seconds_to_expire)) # noqa
        else:
            validated_data['expires_at'] = (validated_data['created_at'] +
                                            timedelta(seconds=13500))

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
