"""
Data models for scoring calculations.

These are simple dataclasses, not Django models.
The scoring engine is pure and doesn't depend on Django ORM.
"""
from dataclasses import dataclass
from typing import List
from decimal import Decimal


@dataclass
class OCBScores:
    """OCB (Order of Card Back) tiebreaker scores."""
    total: int
    last_9: int
    last_6: int
    last_3: int
    last_hole: int

    def as_tuple(self) -> tuple:
        """Return as tuple for sorting."""
        return (self.total, self.last_9, self.last_6, self.last_3, self.last_hole)


@dataclass
class HoleConfiguration:
    """Configuration for a single hole."""
    hole_number: int
    par: int
    stroke_index: int
    distance: int = 0


@dataclass
class CourseConfiguration:
    """Golf course configuration data."""
    course_name: str
    tee_color: str
    holes: List[HoleConfiguration]  # 18 holes
    course_rating: Decimal
    slope_rating: int
    total_par: int


@dataclass
class PlayerRoundScore:
    """Complete scoring data for a player's round."""
    player_id: str
    player_name: str
    handicap: int
    division: str
    hole_scores: List[int]  # 18 values
    gross_score: int
    net_score: int
    ocb_gross: OCBScores
    ocb_net: OCBScores
    rank: int = 0
    rank_division: int = 0
