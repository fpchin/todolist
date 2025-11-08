"""
Tournament serializers for GTMS API.
"""
from rest_framework import serializers
from .models import Tournament, TournamentPlayer, Round, TeeTime, FlightPlayer
from apps.players.serializers import PlayerSerializer
from apps.courses.serializers import CourseConfigurationSerializer


class TournamentSerializer(serializers.ModelSerializer):
    """Serializer for tournament data."""

    player_count = serializers.SerializerMethodField()
    round_count = serializers.SerializerMethodField()

    class Meta:
        model = Tournament
        fields = [
            'id',
            'name',
            'start_date',
            'end_date',
            'location',
            'format_type',
            'status',
            'description',
            'max_players',
            'player_count',
            'round_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_player_count(self, obj):
        """Get number of registered players."""
        return obj.registrations.filter(
            status__in=['REGISTERED', 'CONFIRMED']
        ).count()

    def get_round_count(self, obj):
        """Get number of rounds."""
        return obj.rounds.count()


class TournamentPlayerSerializer(serializers.ModelSerializer):
    """Serializer for tournament player registration."""

    player = PlayerSerializer(read_only=True)
    player_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = TournamentPlayer
        fields = [
            'id',
            'tournament',
            'player',
            'player_id',
            'handicap_index',
            'playing_handicap',
            'division',
            'registration_date',
            'status',
            'created_at'
        ]
        read_only_fields = ['id', 'tournament', 'registration_date', 'created_at']


class RoundSerializer(serializers.ModelSerializer):
    """Serializer for tournament round."""

    course = CourseConfigurationSerializer(read_only=True)
    course_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Round
        fields = [
            'id',
            'tournament',
            'round_number',
            'round_date',
            'course',
            'course_id',
            'status',
            'created_at'
        ]
        read_only_fields = ['id', 'tournament', 'created_at']


class FlightPlayerSerializer(serializers.ModelSerializer):
    """Serializer for flight player."""

    player = PlayerSerializer(read_only=True)
    player_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = FlightPlayer
        fields = [
            'id',
            'tee_time',
            'player',
            'player_id',
            'position'
        ]
        read_only_fields = ['id', 'tee_time']


class TeeTimeSerializer(serializers.ModelSerializer):
    """Serializer for tee time."""

    players = FlightPlayerSerializer(many=True, read_only=True)

    class Meta:
        model = TeeTime
        fields = [
            'id',
            'tournament',
            'round',
            'tee_time',
            'starting_hole',
            'players',
            'created_at'
        ]
        read_only_fields = ['id', 'tournament', 'created_at']


class TournamentDetailSerializer(TournamentSerializer):
    """Detailed tournament serializer with rounds and registrations."""

    rounds = RoundSerializer(many=True, read_only=True)
    registrations = TournamentPlayerSerializer(many=True, read_only=True)

    class Meta(TournamentSerializer.Meta):
        fields = TournamentSerializer.Meta.fields + ['rounds', 'registrations']
