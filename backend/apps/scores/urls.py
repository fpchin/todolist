"""
Score and result URL routing.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'hole-scores', views.HoleScoreViewSet, basename='hole-score')
router.register(r'results', views.ResultViewSet, basename='result')

urlpatterns = [
    path('', include(router.urls)),
]
