"""
Tests for Picture API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..serializers import PictureSerializer
from core.models import Picture # noqa

PICTURES_URL = reverse('picture:picture-list')


def create_picture(user, **params):
    """creates and returns example picture"""
    defaults = {
        'title': 'Test picture title',
        'description': 'Test picture description',
        'link': 'http://www.example.com/picture.jpg'
    }
    defaults.update(params)
    picture = Picture.objects.create(user=user, **defaults)
    return picture


class PublicPictureAPITests(TestCase):
    """represents unauthenticated requests"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """tests if auth is demanded to request"""
        res = self.client.get(PICTURES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePictureAPITest(TestCase):
    """represents tests for authenticated user"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_pictures(self):
        """tests if list of pictures retrieves"""
        create_picture(user=self.user)
        create_picture(user=self.user)
        res = self.client.get(PICTURES_URL)
        pictures = Picture.objects.all().order_by('-id')
        serializer = PictureSerializer(pictures, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_picture_list_limited_to_user(self):
        """tests if user sees just his pictures list"""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'otherpass123'
        )
        create_picture(user=other_user)
        create_picture(user=self.user)
        res = self.client.get(PICTURES_URL)
        pictures = Picture.objects.filter(user=self.user)
        serializer = PictureSerializer(pictures, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
