"""
Tournament URL routing.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tournaments', views.TournamentViewSet, basename='tournament')
router.register(r'tournament-players', views.TournamentPlayerViewSet, basename='tournament-player')
router.register(r'rounds', views.RoundViewSet, basename='round')

urlpatterns = [
    path('', include(router.urls)),
]
