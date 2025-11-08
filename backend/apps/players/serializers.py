"""
Player serializers for GTMS API.
"""
from rest_framework import serializers
from .models import Player, HandicapHistory


class HandicapHistorySerializer(serializers.ModelSerializer):
    """Serializer for handicap history."""

    class Meta:
        model = HandicapHistory
        fields = [
            'id',
            'handicap_index',
            'effective_date',
            'issuing_authority',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class PlayerSerializer(serializers.ModelSerializer):
    """Serializer for player data."""

    full_name = serializers.ReadOnlyField()
    current_handicap = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = [
            'id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone',
            'club_affiliation',
            'date_of_birth',
            'current_handicap',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_current_handicap(self, obj):
        """Get player's current handicap index."""
        latest = obj.handicap_history.first()
        if latest:
            return {
                'handicap_index': float(latest.handicap_index),
                'effective_date': latest.effective_date
            }
        return None


class PlayerDetailSerializer(PlayerSerializer):
    """Detailed player serializer with handicap history."""

    handicap_history = HandicapHistorySerializer(many=True, read_only=True)

    class Meta(PlayerSerializer.Meta):
        fields = PlayerSerializer.Meta.fields + ['handicap_history']
