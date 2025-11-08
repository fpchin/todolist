"""
Score and result serializers for GTMS API.
"""
from rest_framework import serializers
from .models import HoleScore, Result
from apps.players.serializers import PlayerSerializer
from apps.tournaments.serializers import TournamentSerializer


class HoleScoreSerializer(serializers.ModelSerializer):
    """Serializer for hole score."""

    player = PlayerSerializer(read_only=True)
    player_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = HoleScore
        fields = [
            'id',
            'round',
            'player',
            'player_id',
            'hole_number',
            'strokes',
            'putts',
            'fairway_hit',
            'green_in_regulation',
            'penalty_strokes',
            'verified',
            'scorer',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class HoleScoreBulkCreateSerializer(serializers.Serializer):
    """Serializer for bulk hole score creation (all 18 holes at once)."""

    round_id = serializers.UUIDField()
    player_id = serializers.UUIDField()
    hole_scores = serializers.ListField(
        child=serializers.IntegerField(min_value=1, max_value=15),
        min_length=18,
        max_length=18
    )

    def validate_hole_scores(self, value):
        """Validate hole scores list."""
        if len(value) != 18:
            raise serializers.ValidationError("Must provide exactly 18 hole scores")
        return value


class ResultSerializer(serializers.ModelSerializer):
    """Serializer for tournament result."""

    player = PlayerSerializer(read_only=True)
    tournament = TournamentSerializer(read_only=True)

    class Meta:
        model = Result
        fields = [
            'id',
            'tournament',
            'player',
            'division',
            'total_gross',
            'total_net',
            'total_points',
            'gross_last_9',
            'gross_last_6',
            'gross_last_3',
            'gross_last_hole',
            'net_last_9',
            'net_last_6',
            'net_last_3',
            'net_last_hole',
            'rank_overall',
            'rank_division',
            'prize_category',
            'calculated_at',
            'verified'
        ]
        read_only_fields = ['id', 'calculated_at']


class LeaderboardEntrySerializer(serializers.Serializer):
    """Serializer for leaderboard entry."""

    rank = serializers.IntegerField()
    rank_division = serializers.IntegerField()
    player_id = serializers.UUIDField()
    player_name = serializers.CharField()
    division = serializers.CharField()
    gross_score = serializers.IntegerField()
    net_score = serializers.IntegerField()

    # OCB tiebreakers
    last_9 = serializers.IntegerField()
    last_6 = serializers.IntegerField()
    last_3 = serializers.IntegerField()
    last_hole = serializers.IntegerField()

    # Optional detailed stats
    holes_played = serializers.IntegerField(required=False)
    through_hole = serializers.IntegerField(required=False)


class PlayerScorecard Serializer(serializers.Serializer):
    """Serializer for player's scorecard."""

    player = PlayerSerializer()
    round_number = serializers.IntegerField()
    course_name = serializers.CharField()
    handicap = serializers.IntegerField()

    hole_scores = serializers.ListField(
        child=serializers.IntegerField()
    )
    hole_pars = serializers.ListField(
        child=serializers.IntegerField()
    )
    hole_stroke_indices = serializers.ListField(
        child=serializers.IntegerField()
    )

    gross_score = serializers.IntegerField()
    net_score = serializers.IntegerField()

    # Front 9 / Back 9 breakdown
    front_9_gross = serializers.IntegerField()
    front_9_net = serializers.IntegerField()
    back_9_gross = serializers.IntegerField()
    back_9_net = serializers.IntegerField()
