"""
Tests for models
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from .. import models
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch


class ModelTests(TestCase):
    """Test models"""
    def test_create_user_with_email_successful(self):
        """tests successful creating user with email"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """tests if email normalized correctly"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'testpass123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """tests if creating user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'testpass123')

    def test_create_superuser(self):
        """tets superuser creating"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'testpass123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.role, 'Admin')

    def test_create_picture(self):
        """tests if picture object in db creating is successful"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )
        picture = models.Picture.objects.create(
            user=user,
            title='Test picture name',
            description='Some sample description',
            created_at=timezone.now(),
            expires_at=timezone.now() + timedelta(seconds=3600),
        )

        self.assertEqual(str(picture), picture.title)

    @patch('core.models.uuid.uuid4')
    def test_image_filename_uuid(self, mock_uuid):
        """tests generating uuid path"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/picture/{uuid}.jpg')
