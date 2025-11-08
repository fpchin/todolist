"""
Player URL routing.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'players', views.PlayerViewSet, basename='player')

urlpatterns = [
    path('', include(router.urls)),
]
