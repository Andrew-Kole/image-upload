"""
Tests for Picture API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..serializers import (
    PictureSerializer,
    PictureDetailSerializer,
)
from core.models import Picture # noqa

PICTURES_URL = reverse('picture:picture-list')


def detail_url(picture_id):
    """creates and returns picture detail URL"""
    return reverse('picture:picture-detail', args=[picture_id])


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


def create_user(**params):
    """creats and returns user"""
    return get_user_model().objects.create_user(**params)


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
        self.user = create_user(email='test@example.com', password='testpass123')
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
        other_user = create_user(email='other@example.com', password='otherpass123')
        create_picture(user=other_user)
        create_picture(user=self.user)
        res = self.client.get(PICTURES_URL)
        pictures = Picture.objects.filter(user=self.user)
        serializer = PictureSerializer(pictures, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_picture_detail(self):
        """Test of getting picture detail"""
        picture = create_picture(user=self.user)
        url = detail_url(picture.id)
        res = self.client.get(url)
        serializer = PictureDetailSerializer(picture)

        self.assertEqual(res.data, serializer.data)

    def test_create_picture(self):
        """tests creating of picture"""
        payload = {
            'title': 'Test title',
            'link': 'https://www.example.com'
        }
        res = self.client.post(PICTURES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        picture = Picture.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(picture, k), v)
        self.assertEqual(picture.user, self.user)

    def test_partial_update(self):
        """tests partial update of picture"""
        original_link = 'https://www.example.com'
        picture = create_picture(
            user=self.user,
            title='Test picture title',
            link=original_link,
        )
        payload = {'title': 'New picture title'}
        url = detail_url(picture.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        picture.refresh_from_db()

        self.assertEqual(picture.title, payload['title'])
        self.assertEqual(picture.link, original_link)
        self.assertEqual(picture.user, self.user)

    def test_full_update(self):
        """tests ful update of picture"""
        picture = create_picture(
            user=self.user,
            title='Test picture title',
            link='https://www.example.com',
            description='Test picture description',
        )
        payload = {
            'title': 'New picture title',
            'link': 'https://www.google.com',
            'description': 'New picture description',
        }
        url = detail_url(picture.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        picture.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(picture, k), v)
        self.assertEqual(picture.user, self.user)

    def test_delete_picture(self):
        """tests if deleting picture works correctly"""
        picture = create_picture(user=self.user)
        url = detail_url(picture.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Picture.objects.filter(id=picture.id).exists())
