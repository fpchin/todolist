"""
Data validators for migration
"""
import logging
from typing import Dict, Any, List, Tuple
from datetime import datetime, date

logger = logging.getLogger(__name__)


class MigrationValidator:
    """Validate parsed data before database import"""

    def __init__(self):
        self.errors = []
        self.warnings = []

    def validate_all(self, data: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """Validate all data sections"""
        self.errors = []
        self.warnings = []

        self.validate_tournament(data.get('tournament', {}))
        self.validate_course(data.get('course', {}))
        self.validate_players(data.get('players', []))
        self.validate_scores(data.get('scores', []))

        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings

    def validate_tournament(self, tournament: Dict[str, Any]) -> None:
        """Validate tournament data"""
        if not tournament:
            self.errors.append("Tournament data is empty")
            return

        # Required fields
        if not tournament.get('name'):
            self.errors.append("Tournament name is required")

        if not tournament.get('location'):
            self.warnings.append("Tournament location is missing")

        # Dates
        start_date = tournament.get('start_date')
        end_date = tournament.get('end_date')

        if not start_date:
            self.warnings.append("Tournament start date is missing")
        elif isinstance(start_date, str):
            try:
                tournament['start_date'] = datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                self.errors.append(f"Invalid start date format: {start_date}")

        if not end_date:
            self.warnings.append("Tournament end date is missing")
        elif isinstance(end_date, str):
            try:
                tournament['end_date'] = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                self.errors.append(f"Invalid end date format: {end_date}")

        # Validate date order
        if start_date and end_date:
            if isinstance(start_date, date) and isinstance(end_date, date):
                if end_date < start_date:
                    self.errors.append("End date cannot be before start date")

        # Format type
        valid_formats = ['STROKEPLAY', 'STABLEFORD', 'MATCHPLAY', 'SCRAMBLE']
        format_type = tournament.get('format_type', 'STROKEPLAY')
        if format_type not in valid_formats:
            self.warnings.append(f"Unknown format type: {format_type}, defaulting to STROKEPLAY")
            tournament['format_type'] = 'STROKEPLAY'

        # Max players
        max_players = tournament.get('max_players', 200)
        if not isinstance(max_players, int) or max_players < 1:
            self.warnings.append(f"Invalid max_players: {max_players}, defaulting to 200")
            tournament['max_players'] = 200

    def validate_course(self, course: Dict[str, Any]) -> None:
        """Validate course configuration"""
        if not course:
            self.errors.append("Course data is empty")
            return

        holes = course.get('holes', [])
        if not holes:
            self.errors.append("Course has no holes defined")
            return

        if len(holes) != 18:
            self.errors.append(f"Course must have exactly 18 holes, found {len(holes)}")

        # Validate each hole
        hole_numbers = set()
        for i, hole in enumerate(holes):
            hole_num = hole.get('hole_number')
            if not hole_num:
                self.errors.append(f"Hole {i+1} is missing hole_number")
                continue

            if hole_num in hole_numbers:
                self.errors.append(f"Duplicate hole number: {hole_num}")
            hole_numbers.add(hole_num)

            # Par validation
            par = hole.get('par')
            if not par or par < 3 or par > 5:
                self.errors.append(f"Hole {hole_num} has invalid par: {par}")

            # Stroke index
            si = hole.get('handicap_stroke_index')
            if not si or si < 1 or si > 18:
                self.errors.append(f"Hole {hole_num} has invalid stroke index: {si}")

        # Validate we have all 18 hole numbers
        if len(hole_numbers) == 18 and hole_numbers != set(range(1, 19)):
            self.errors.append("Hole numbers must be 1-18")

        # Validate total par
        total_par = sum(h.get('par', 0) for h in holes)
        if total_par != course.get('par'):
            self.warnings.append(f"Course par {course.get('par')} doesn't match sum of hole pars {total_par}")
            course['par'] = total_par

    def validate_players(self, players: List[Dict[str, Any]]) -> None:
        """Validate player data"""
        if not players:
            self.warnings.append("No players found in data")
            return

        seen_emails = set()
        for i, player in enumerate(players):
            # Name validation
            if not player.get('first_name') and not player.get('last_name'):
                self.errors.append(f"Player {i+1} has no name")

            # Email validation
            email = player.get('email')
            if not email:
                self.errors.append(f"Player {i+1} ({player.get('first_name')} {player.get('last_name')}) has no email")
            elif email in seen_emails:
                self.errors.append(f"Duplicate email: {email}")
            else:
                seen_emails.add(email)

            # Handicap validation
            hcp = player.get('handicap_index')
            if hcp is None:
                self.warnings.append(f"Player {email} has no handicap")
            elif not isinstance(hcp, (int, float)):
                self.errors.append(f"Player {email} has invalid handicap: {hcp}")
            elif hcp < 0 or hcp > 54:
                self.warnings.append(f"Player {email} has unusual handicap: {hcp}")

    def validate_scores(self, scores: List[Dict[str, Any]]) -> None:
        """Validate score data"""
        if not scores:
            self.warnings.append("No scores found in data")
            return

        for score in scores:
            # Validate hole number
            hole_num = score.get('hole_number')
            if not hole_num or hole_num < 1 or hole_num > 18:
                self.errors.append(f"Invalid hole number: {hole_num}")

            # Validate strokes
            strokes = score.get('strokes')
            if not strokes or strokes < 1 or strokes > 20:
                self.errors.append(f"Invalid strokes for hole {hole_num}: {strokes}")

    def get_summary(self) -> str:
        """Get validation summary"""
        summary = []
        summary.append(f"Validation Results:")
        summary.append(f"  Errors: {len(self.errors)}")
        summary.append(f"  Warnings: {len(self.warnings)}")

        if self.errors:
            summary.append("\nErrors:")
            for error in self.errors:
                summary.append(f"  - {error}")

        if self.warnings:
            summary.append("\nWarnings:")
            for warning in self.warnings:
                summary.append(f"  - {warning}")

        return '\n'.join(summary)
