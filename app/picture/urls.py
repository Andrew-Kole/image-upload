"""
URL mappings for Picture app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('pictures', views.PictureViewSet)
app_name = 'picture'
urlpatterns = [
    path('', include(router.urls)),
]
