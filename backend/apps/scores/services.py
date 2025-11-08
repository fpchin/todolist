"""
Score calculation services integrating the scoring engine.
"""
from typing import List, Dict
from django.db.models import Q
from apps.scoring import engine
from apps.scoring.models import PlayerRoundScore, OCBScores
from .models import HoleScore, Result
from apps.tournaments.models import Tournament, TournamentPlayer, Round


class ScoringService:
    """Service for calculating scores using the scoring engine."""

    def calculate_player_round_score(
        self,
        round_id: str,
        player_id: str
    ) -> PlayerRoundScore:
        """
        Calculate gross and net scores for a player's round.

        Args:
            round_id: Round UUID
            player_id: Player UUID

        Returns:
            PlayerRoundScore object with all calculated values
        """
        # Fetch round and player data
        round_obj = Round.objects.select_related(
            'course', 'tournament'
        ).get(id=round_id)

        tournament_player = TournamentPlayer.objects.select_related(
            'player'
        ).get(
            tournament=round_obj.tournament,
            player_id=player_id
        )

        # Get hole scores
        hole_scores = list(
            HoleScore.objects.filter(
                round_id=round_id,
                player_id=player_id
            ).order_by('hole_number').values_list('strokes', flat=True)
        )

        if len(hole_scores) != 18:
            raise ValueError(f"Player has only {len(hole_scores)} hole scores (need 18)")

        # Get course stroke indices
        stroke_indices = round_obj.course.stroke_indices

        # Calculate using scoring engine
        gross_score = engine.calculate_gross_score(hole_scores)
        net_score = engine.calculate_net_score(
            hole_scores,
            tournament_player.playing_handicap,
            stroke_indices
        )
        ocb_gross = engine.calculate_ocb_gross(hole_scores)
        ocb_net = engine.calculate_ocb_net(
            hole_scores,
            tournament_player.playing_handicap,
            stroke_indices
        )

        return PlayerRoundScore(
            player_id=str(player_id),
            player_name=tournament_player.player.full_name,
            handicap=tournament_player.playing_handicap,
            division=tournament_player.division,
            hole_scores=hole_scores,
            gross_score=gross_score,
            net_score=net_score,
            ocb_gross=ocb_gross,
            ocb_net=ocb_net
        )

    def calculate_tournament_results(self, tournament_id: str) -> List[Result]:
        """
        Calculate results for all players in a tournament.

        Args:
            tournament_id: Tournament UUID

        Returns:
            List of Result objects
        """
        tournament = Tournament.objects.get(id=tournament_id)
        rounds = tournament.rounds.all()

        # Get all registered players
        tournament_players = TournamentPlayer.objects.filter(
            tournament_id=tournament_id,
            status__in=['REGISTERED', 'CONFIRMED']
        ).select_related('player')

        player_scores = []

        for tp in tournament_players:
            # Calculate scores for all rounds
            try:
                # For now, assuming single round; multi-round support coming
                round_obj = rounds.first()
                if not round_obj:
                    continue

                score = self.calculate_player_round_score(
                    round_obj.id,
                    tp.player.id
                )
                player_scores.append(score)
            except (HoleScore.DoesNotExist, ValueError):
                # Player hasn't completed all holes yet
                continue

        # Rank players
        ranked = engine.rank_players(player_scores, use_net_scores=True)

        # Create/update Result objects
        results = []
        for player_score in ranked:
            result, created = Result.objects.update_or_create(
                tournament_id=tournament_id,
                player_id=player_score.player_id,
                defaults={
                    'division': player_score.division,
                    'total_gross': player_score.gross_score,
                    'total_net': player_score.net_score,
                    'gross_last_9': player_score.ocb_gross.last_9,
                    'gross_last_6': player_score.ocb_gross.last_6,
                    'gross_last_3': player_score.ocb_gross.last_3,
                    'gross_last_hole': player_score.ocb_gross.last_hole,
                    'net_last_9': player_score.ocb_net.last_9,
                    'net_last_6': player_score.ocb_net.last_6,
                    'net_last_3': player_score.ocb_net.last_3,
                    'net_last_hole': player_score.ocb_net.last_hole,
                    'rank_overall': player_score.rank,
                    'rank_division': player_score.rank_division,
                }
            )
            results.append(result)

        return results


class LeaderboardService:
    """Service for generating leaderboards."""

    def get_tournament_leaderboard(
        self,
        tournament_id: str,
        division: str = None
    ) -> List[Dict]:
        """
        Get tournament leaderboard.

        Args:
            tournament_id: Tournament UUID
            division: Optional division filter

        Returns:
            List of leaderboard entries
        """
        query = Result.objects.filter(
            tournament_id=tournament_id
        ).select_related('player').order_by('rank_overall')

        if division:
            query = query.filter(division=division)

        leaderboard = []
        for result in query:
            leaderboard.append({
                'rank': result.rank_overall,
                'rank_division': result.rank_division,
                'player_id': str(result.player.id),
                'player_name': result.player.full_name,
                'division': result.division,
                'gross_score': result.total_gross,
                'net_score': result.total_net,
                'last_9': result.net_last_9,
                'last_6': result.net_last_6,
                'last_3': result.net_last_3,
                'last_hole': result.net_last_hole,
            })

        return leaderboard

    def get_live_leaderboard(
        self,
        tournament_id: str,
        division: str = None
    ) -> List[Dict]:
        """
        Get live leaderboard (recalculated on demand).

        Args:
            tournament_id: Tournament UUID
            division: Optional division filter

        Returns:
            List of leaderboard entries with latest scores
        """
        scoring_service = ScoringService()

        # Recalculate all results
        scoring_service.calculate_tournament_results(tournament_id)

        # Return leaderboard
        return self.get_tournament_leaderboard(tournament_id, division)
