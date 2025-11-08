"""
Player API views.
"""
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Player
from .serializers import PlayerSerializer, PlayerDetailSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    """ViewSet for player CRUD operations."""

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['last_name', 'first_name', 'created_at']
    ordering = ['last_name', 'first_name']

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'retrieve':
            return PlayerDetailSerializer
        return PlayerSerializer
