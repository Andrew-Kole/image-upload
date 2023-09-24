"""
DB models
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin)
from django.conf import settings
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom manager for users"""
    def create_user(self, email, password=None, **extra_fields):
        """creates, saves and returns a new user"""
        if not email:
            raise ValueError('Provide email!')
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """creates a superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.role = 'Admin'
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """represents user model"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    role_choices = (
        ('Basic', 'Basic'),
        ('Premium', 'Premium'),
        ('Enterprise', 'Enterprise'),
        ('Admin', 'Admin'),
    )
    role = models.CharField(max_length=50, choices=role_choices,
                            default='Basic')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Picture(models.Model):
    """represents picture model"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link = models.URLField()
    created_at = models.DateTimeField(default=timezone.now)
    expiration = timezone.now() + timezone.timedelta(seconds=13500)
    expires_at = models.DateTimeField(default=expiration)

    def __str__(self):
        return self.title
