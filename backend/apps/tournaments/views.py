"""
Tournament API views.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Tournament, TournamentPlayer, Round
from .serializers import (
    TournamentSerializer,
    TournamentDetailSerializer,
    TournamentPlayerSerializer,
    RoundSerializer
)


class TournamentViewSet(viewsets.ModelViewSet):
    """ViewSet for tournament CRUD operations."""

    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'format_type']
    search_fields = ['name', 'location']
    ordering_fields = ['start_date', 'name']
    ordering = ['-start_date']

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'retrieve':
            return TournamentDetailSerializer
        return TournamentSerializer

    @action(detail=True, methods=['post'])
    def register_player(self, request, pk=None):
        """Register a player for the tournament."""
        tournament = self.get_object()

        # Check if tournament is open for registration
        if tournament.status not in ['DRAFT', 'OPEN']:
            return Response(
                {'error': 'Tournament is not open for registration'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TournamentPlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tournament=tournament)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def players(self, request, pk=None):
        """Get all registered players for this tournament."""
        tournament = self.get_object()
        players = tournament.registrations.all()
        serializer = TournamentPlayerSerializer(players, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def leaderboard(self, request, pk=None):
        """Get tournament leaderboard."""
        tournament = self.get_object()

        # Import here to avoid circular dependency
        from apps.scores.services import LeaderboardService

        leaderboard_service = LeaderboardService()
        leaderboard = leaderboard_service.get_tournament_leaderboard(tournament.id)

        return Response(leaderboard)


class TournamentPlayerViewSet(viewsets.ModelViewSet):
    """ViewSet for tournament player registrations."""

    queryset = TournamentPlayer.objects.all()
    serializer_class = TournamentPlayerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tournament', 'player', 'division', 'status']


class RoundViewSet(viewsets.ModelViewSet):
    """ViewSet for tournament rounds."""

    queryset = Round.objects.all()
    serializer_class = RoundSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tournament', 'status']
