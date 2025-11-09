"""
Tests for scoring services
"""
import pytest
from apps.scores.services import ScoringService, LeaderboardService
from apps.scores.models import Result


@pytest.mark.django_db
class TestScoringService:
    """Test ScoringService"""

    def test_calculate_player_round_score(self, round_obj, player, tournament_player, hole_scores):
        """Test calculating player round score"""
        service = ScoringService()

        player_score = service.calculate_player_round_score(
            str(round_obj.id),
            str(player.id)
        )

        assert player_score.player_id == str(player.id)
        assert player_score.player_name == player.full_name
        assert player_score.handicap == tournament_player.playing_handicap
        assert player_score.gross_score > 0
        assert player_score.net_score > 0
        assert player_score.ocb_gross.total == player_score.gross_score

    def test_calculate_tournament_results(self, tournament, round_obj, tournament_player, hole_scores):
        """Test calculating tournament results"""
        service = ScoringService()

        results = service.calculate_tournament_results(str(tournament.id))

        assert len(results) == 1
        assert results[0].player == tournament_player.player
        assert results[0].total_gross > 0
        assert results[0].total_net > 0
        assert results[0].rank_overall == 1

    def test_ocb_calculation(self, round_obj, player, tournament_player, hole_scores):
        """Test OCB tiebreaker calculation"""
        service = ScoringService()

        player_score = service.calculate_player_round_score(
            str(round_obj.id),
            str(player.id)
        )

        # Verify OCB values are calculated
        assert player_score.ocb_gross.last_9 > 0
        assert player_score.ocb_gross.last_6 > 0
        assert player_score.ocb_gross.last_3 > 0
        assert player_score.ocb_gross.last_hole > 0

        assert player_score.ocb_net.last_9 > 0
        assert player_score.ocb_net.last_6 > 0
        assert player_score.ocb_net.last_3 > 0
        assert player_score.ocb_net.last_hole > 0


@pytest.mark.django_db
class TestLeaderboardService:
    """Test LeaderboardService"""

    def test_get_tournament_leaderboard(self, tournament, round_obj, tournament_player, hole_scores):
        """Test getting tournament leaderboard"""
        # First calculate results
        scoring_service = ScoringService()
        scoring_service.calculate_tournament_results(str(tournament.id))

        # Then get leaderboard
        leaderboard_service = LeaderboardService()
        leaderboard = leaderboard_service.get_tournament_leaderboard(str(tournament.id))

        assert 'tournament' in leaderboard
        assert 'entries' in leaderboard
        assert len(leaderboard['entries']) == 1
        assert leaderboard['entries'][0]['rank_overall'] == 1

    def test_get_live_leaderboard(self, tournament, round_obj, tournament_player, hole_scores):
        """Test getting live leaderboard (recalculated)"""
        leaderboard_service = LeaderboardService()
        leaderboard = leaderboard_service.get_live_leaderboard(str(tournament.id))

        assert 'tournament' in leaderboard
        assert 'entries' in leaderboard
        assert len(leaderboard['entries']) == 1
