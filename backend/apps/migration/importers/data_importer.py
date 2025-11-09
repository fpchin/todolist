"""
Data importer for legacy Excel data
"""
import logging
from typing import Dict, Any, List
from django.db import transaction
from decimal import Decimal

from apps.tournaments.models import Tournament, TournamentPlayer, Round
from apps.players.models import Player
from apps.courses.models import CourseConfiguration, HoleConfiguration
from apps.scores.models import HoleScore

logger = logging.getLogger(__name__)


class DataImporter:
    """Import validated data into database"""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.stats = {
            'tournaments_created': 0,
            'courses_created': 0,
            'players_created': 0,
            'tournament_players_created': 0,
            'rounds_created': 0,
            'scores_created': 0,
        }

    def import_data(self, data: Dict[str, Any]) -> Dict[str, int]:
        """Import all data sections"""
        if self.dry_run:
            logger.info("DRY RUN MODE - No database changes will be made")

        try:
            with transaction.atomic():
                # Import in dependency order
                course = self._import_course(data.get('course', {}))
                tournament = self._import_tournament(data.get('tournament', {}))
                players = self._import_players(data.get('players', []))
                tournament_players = self._import_tournament_players(
                    tournament, players, data.get('players', [])
                )
                round_obj = self._create_round(tournament, course)
                self._import_scores(round_obj, players, data.get('scores', []))

                if self.dry_run:
                    logger.info("Dry run complete - rolling back transaction")
                    raise Exception("Dry run - rollback")

        except Exception as e:
            if self.dry_run and "Dry run" in str(e):
                logger.info("Dry run successful - data is valid")
            else:
                logger.error(f"Import failed: {e}")
                raise

        return self.stats

    def _import_tournament(self, tournament_data: Dict[str, Any]) -> Tournament:
        """Import tournament"""
        tournament = Tournament.objects.create(
            name=tournament_data.get('name', 'Imported Tournament'),
            location=tournament_data.get('location', 'Unknown'),
            start_date=tournament_data.get('start_date'),
            end_date=tournament_data.get('end_date'),
            format_type=tournament_data.get('format_type', 'STROKEPLAY'),
            status=tournament_data.get('status', 'COMPLETED'),
            max_players=tournament_data.get('max_players', 200),
        )
        self.stats['tournaments_created'] += 1
        logger.info(f"Created tournament: {tournament.name}")
        return tournament

    def _import_course(self, course_data: Dict[str, Any]) -> CourseConfiguration:
        """Import course configuration"""
        course = CourseConfiguration.objects.create(
            course_name=course_data.get('course_name', 'Imported Course'),
            tee_color=course_data.get('tee_color', 'White'),
            rating=Decimal(str(course_data.get('rating', 72.0))),
            slope=course_data.get('slope', 113),
            par=course_data.get('par', 72),
        )
        self.stats['courses_created'] += 1

        # Import holes
        holes_data = course_data.get('holes', [])
        for hole_data in holes_data:
            HoleConfiguration.objects.create(
                course=course,
                hole_number=hole_data['hole_number'],
                par=hole_data['par'],
                handicap_stroke_index=hole_data['handicap_stroke_index'],
                distance=hole_data['distance'],
            )

        logger.info(f"Created course: {course.course_name} with {len(holes_data)} holes")
        return course

    def _import_players(self, players_data: List[Dict[str, Any]]) -> Dict[str, Player]:
        """Import players"""
        players = {}

        for player_data in players_data:
            email = player_data.get('email')
            if not email:
                continue

            # Check if player already exists
            player = Player.objects.filter(email=email).first()
            if not player:
                player = Player.objects.create(
                    first_name=player_data.get('first_name', ''),
                    last_name=player_data.get('last_name', ''),
                    email=email,
                    phone=player_data.get('phone', ''),
                    club_affiliation=player_data.get('club_affiliation', ''),
                )
                self.stats['players_created'] += 1

            players[email] = player

        logger.info(f"Imported {len(players)} players")
        return players

    def _import_tournament_players(
        self,
        tournament: Tournament,
        players: Dict[str, Player],
        players_data: List[Dict[str, Any]]
    ) -> Dict[str, TournamentPlayer]:
        """Import tournament player registrations"""
        tournament_players = {}

        for player_data in players_data:
            email = player_data.get('email')
            if not email or email not in players:
                continue

            player = players[email]
            handicap_index = Decimal(str(player_data.get('handicap_index', 0.0)))

            # Calculate playing handicap (simplified - should use proper calculation)
            playing_handicap = int(handicap_index)

            tournament_player = TournamentPlayer.objects.create(
                tournament=tournament,
                player=player,
                handicap_index=handicap_index,
                playing_handicap=playing_handicap,
                division=player_data.get('division', 'Championship'),
                status='CONFIRMED',
            )
            self.stats['tournament_players_created'] += 1
            tournament_players[email] = tournament_player

        logger.info(f"Registered {len(tournament_players)} players to tournament")
        return tournament_players

    def _create_round(self, tournament: Tournament, course: CourseConfiguration) -> Round:
        """Create a round for the tournament"""
        round_obj = Round.objects.create(
            tournament=tournament,
            round_number=1,
            round_date=tournament.start_date,
            course=course,
            status='COMPLETED',
        )
        self.stats['rounds_created'] += 1
        logger.info(f"Created round 1 for tournament")
        return round_obj

    def _import_scores(
        self,
        round_obj: Round,
        players: Dict[str, Player],
        scores_data: List[Dict[str, Any]]
    ) -> None:
        """Import hole scores"""
        if not scores_data:
            logger.info("No scores to import")
            return

        for score_data in scores_data:
            player_email = score_data.get('player_email')
            if not player_email or player_email not in players:
                continue

            player = players[player_email]

            HoleScore.objects.create(
                round=round_obj,
                player=player,
                hole_number=score_data['hole_number'],
                strokes=score_data['strokes'],
                putts=score_data.get('putts'),
                fairway_hit=score_data.get('fairway_hit'),
                green_in_regulation=score_data.get('green_in_regulation'),
                verified=True,
            )
            self.stats['scores_created'] += 1

        logger.info(f"Imported {self.stats['scores_created']} hole scores")

    def get_summary(self) -> str:
        """Get import summary"""
        summary = []
        summary.append("Import Summary:")
        summary.append(f"  Tournaments created: {self.stats['tournaments_created']}")
        summary.append(f"  Courses created: {self.stats['courses_created']}")
        summary.append(f"  Players created: {self.stats['players_created']}")
        summary.append(f"  Tournament players: {self.stats['tournament_players_created']}")
        summary.append(f"  Rounds created: {self.stats['rounds_created']}")
        summary.append(f"  Scores imported: {self.stats['scores_created']}")
        return '\n'.join(summary)
