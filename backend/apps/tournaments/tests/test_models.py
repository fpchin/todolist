"""
Tests for tournament models
"""
import pytest
from decimal import Decimal
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from apps.tournaments.models import Tournament, TournamentPlayer, Round


@pytest.mark.django_db
class TestTournamentModel:
    """Test Tournament model"""

    def test_create_tournament(self, tournament):
        """Test tournament creation"""
        assert tournament.name == 'Test Championship 2023'
        assert tournament.status == 'OPEN'
        assert tournament.max_players == 200
        assert str(tournament) == 'Test Championship 2023'

    def test_tournament_str_representation(self, tournament):
        """Test string representation"""
        assert str(tournament) == tournament.name

    def test_tournament_date_validation(self, db):
        """Test that end_date must be after start_date"""
        with pytest.raises(Exception):  # Should raise validation error
            Tournament.objects.create(
                name='Invalid Tournament',
                location='Test',
                start_date=date.today(),
                end_date=date.today() - timedelta(days=1),  # End before start
                format_type='STROKEPLAY',
                status='DRAFT'
            )

    def test_tournament_format_choices(self, db):
        """Test valid format types"""
        valid_formats = ['STROKEPLAY', 'STABLEFORD', 'MATCHPLAY', 'SCRAMBLE']

        for fmt in valid_formats:
            tournament = Tournament.objects.create(
                name=f'Test {fmt}',
                location='Test',
                start_date=date.today(),
                end_date=date.today(),
                format_type=fmt,
                status='DRAFT'
            )
            assert tournament.format_type == fmt


@pytest.mark.django_db
class TestTournamentPlayerModel:
    """Test TournamentPlayer model"""

    def test_create_tournament_player(self, tournament_player):
        """Test tournament player creation"""
        assert tournament_player.handicap_index == Decimal('12.5')
        assert tournament_player.playing_handicap == 12
        assert tournament_player.division == 'Championship'
        assert tournament_player.status == 'CONFIRMED'

    def test_tournament_player_unique_constraint(self, tournament, player):
        """Test player can only register once per tournament"""
        from apps.tournaments.models import TournamentPlayer

        TournamentPlayer.objects.create(
            tournament=tournament,
            player=player,
            handicap_index=Decimal('10.0'),
            playing_handicap=10,
            division='A Division'
        )

        # Trying to register same player again should fail
        with pytest.raises(Exception):
            TournamentPlayer.objects.create(
                tournament=tournament,
                player=player,
                handicap_index=Decimal('15.0'),
                playing_handicap=15,
                division='B Division'
            )


@pytest.mark.django_db
class TestRoundModel:
    """Test Round model"""

    def test_create_round(self, round_obj):
        """Test round creation"""
        assert round_obj.round_number == 1
        assert round_obj.status == 'IN_PROGRESS'
        assert round_obj.course is not None

    def test_round_str_representation(self, round_obj):
        """Test string representation"""
        expected = f"Round {round_obj.round_number} - {round_obj.tournament.name}"
        assert str(round_obj) == expected
