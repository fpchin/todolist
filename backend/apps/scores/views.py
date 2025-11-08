"""
Score and result API views.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import HoleScore, Result
from .serializers import (
    HoleScoreSerializer,
    HoleScoreBulkCreateSerializer,
    ResultSerializer,
    LeaderboardEntrySerializer
)
from .services import ScoringService, LeaderboardService


class HoleScoreViewSet(viewsets.ModelViewSet):
    """ViewSet for hole score CRUD operations."""

    queryset = HoleScore.objects.all()
    serializer_class = HoleScoreSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['round', 'player', 'hole_number', 'verified']

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create all 18 hole scores at once."""
        serializer = HoleScoreBulkCreateSerializer(data=request.data)

        if serializer.is_valid():
            round_id = serializer.validated_data['round_id']
            player_id = serializer.validated_data['player_id']
            hole_scores = serializer.validated_data['hole_scores']

            # Create HoleScore objects for all 18 holes
            created_scores = []
            for hole_num, strokes in enumerate(hole_scores, 1):
                hole_score, created = HoleScore.objects.update_or_create(
                    round_id=round_id,
                    player_id=player_id,
                    hole_number=hole_num,
                    defaults={'strokes': strokes}
                )
                created_scores.append(hole_score)

            # Serialize and return
            output_serializer = HoleScoreSerializer(created_scores, many=True)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResultViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for tournament results (read-only)."""

    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tournament', 'player', 'division']

    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """Recalculate results for a tournament."""
        tournament_id = request.data.get('tournament_id')

        if not tournament_id:
            return Response(
                {'error': 'tournament_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        scoring_service = ScoringService()
        try:
            results = scoring_service.calculate_tournament_results(tournament_id)
            serializer = ResultSerializer(results, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
