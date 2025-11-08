"""
Golf Tournament Scoring Engine

Pure functions for calculating gross scores, net scores, OCB tiebreakers,
and player rankings. This module is isolated from Django ORM for testability.

Based on legacy system: 21ST SIBU AMATEUR OPEN GOLF CHAMPIONSHIP 2023.xlsm
"""
from typing import List, Tuple
from .models import OCBScores, PlayerRoundScore
from .exceptions import (
    InvalidHoleCountError,
    InvalidScoreError,
    InvalidHandicapError,
    InvalidStrokeIndexError
)


def validate_hole_scores(hole_scores: List[int]) -> None:
    """
    Validate hole scores are within acceptable range.

    Args:
        hole_scores: List of 18 hole scores

    Raises:
        InvalidHoleCountError: If not exactly 18 holes
        InvalidScoreError: If any score < 1 or > 15
    """
    if len(hole_scores) != 18:
        raise InvalidHoleCountError(
            f"Expected 18 hole scores, got {len(hole_scores)}"
        )

    for i, score in enumerate(hole_scores, 1):
        if score < 1 or score > 15:
            raise InvalidScoreError(
                f"Hole {i} score {score} is invalid (must be 1-15)"
            )


def validate_stroke_indices(stroke_indices: List[int]) -> None:
    """
    Validate stroke indices are valid (1-18, no duplicates).

    Args:
        stroke_indices: List of 18 stroke indices

    Raises:
        InvalidStrokeIndexError: If indices are invalid
    """
    if len(stroke_indices) != 18:
        raise InvalidStrokeIndexError(
            f"Expected 18 stroke indices, got {len(stroke_indices)}"
        )

    if set(stroke_indices) != set(range(1, 19)):
        raise InvalidStrokeIndexError(
            "Stroke indices must be 1-18 with no duplicates"
        )


def validate_handicap(handicap: int) -> None:
    """
    Validate handicap is within acceptable range.

    Args:
        handicap: Player's course handicap

    Raises:
        InvalidHandicapError: If handicap < 0 or > 54
    """
    if handicap < 0 or handicap > 54:
        raise InvalidHandicapError(
            f"Handicap {handicap} is invalid (must be 0-54)"
        )


def calculate_gross_score(hole_scores: List[int]) -> int:
    """
    Calculate gross score from hole scores.

    Formula (legacy): AA8 = SUM(E8:V8)

    Args:
        hole_scores: List of 18 integers representing strokes per hole

    Returns:
        Total gross score (sum of all hole scores)

    Raises:
        InvalidHoleCountError: If hole_scores length != 18
        InvalidScoreError: If any score is out of range
    """
    validate_hole_scores(hole_scores)
    return sum(hole_scores)


def calculate_net_hole_score(
    gross_hole_score: int,
    player_handicap: int,
    hole_stroke_index: int
) -> int:
    """
    Calculate net score for a single hole.

    Formula (legacy): Net = Gross - IF(Player_HCP >= Hole_Index, 1, 0)
    Example: AA8 = I8 - IF($C8 - AA$5 >= 0, 1, 0)

    Args:
        gross_hole_score: Strokes taken on this hole
        player_handicap: Player's course handicap
        hole_stroke_index: Hole's stroke index (1-18)

    Returns:
        Net score for this hole (gross - strokes received)
    """
    strokes_received = 1 if player_handicap >= hole_stroke_index else 0
    return gross_hole_score - strokes_received


def get_strokes_received_per_hole(
    player_handicap: int,
    hole_stroke_indices: List[int]
) -> List[int]:
    """
    Calculate strokes received on each hole.

    For handicaps > 18, players receive multiple strokes on harder holes.
    Example: Handicap 24 = 1 stroke on all 18 holes + extra stroke on index 1-6

    Args:
        player_handicap: Player's course handicap
        hole_stroke_indices: Stroke index for each hole (1-18)

    Returns:
        List of strokes received per hole (0, 1, 2, ...)
    """
    validate_handicap(player_handicap)
    validate_stroke_indices(hole_stroke_indices)

    strokes_per_hole = []

    for hole_idx in hole_stroke_indices:
        # Calculate how many "cycles" through 18 holes
        full_cycles = player_handicap // 18  # 0, 1, 2, ...
        remainder = player_handicap % 18

        # Add 1 stroke if this hole's index is within the remainder
        strokes = full_cycles
        if remainder >= hole_idx:
            strokes += 1

        strokes_per_hole.append(strokes)

    return strokes_per_hole


def calculate_net_score(
    hole_scores: List[int],
    player_handicap: int,
    hole_stroke_indices: List[int]
) -> int:
    """
    Calculate total net score for a round.

    Formula (legacy): AS8 = SUM(W8:AN8) where each cell is net hole score

    Args:
        hole_scores: List of 18 gross hole scores
        player_handicap: Player's course handicap
        hole_stroke_indices: List of 18 stroke indices (one per hole)

    Returns:
        Total net score

    Raises:
        InvalidHoleCountError: If not 18 holes
        InvalidScoreError: If scores are invalid
        InvalidHandicapError: If handicap is invalid
    """
    validate_hole_scores(hole_scores)
    validate_handicap(player_handicap)
    validate_stroke_indices(hole_stroke_indices)

    net_hole_scores = [
        calculate_net_hole_score(gross, player_handicap, idx)
        for gross, idx in zip(hole_scores, hole_stroke_indices)
    ]

    return sum(net_hole_scores)


def calculate_ocb_gross(hole_scores: List[int]) -> OCBScores:
    """
    Calculate OCB (Order of Card Back) tiebreaker values for gross scores.

    Legacy formulas (D1Gocb sheet):
        W8 (Last9)  = SUM(N8:V8)   # Holes 10-18
        X8 (Last6)  = SUM(Q8:V8)   # Holes 13-18
        Y8 (Last3)  = SUM(T8:V8)   # Holes 16-18
        Z8 (H18)    = V8           # Hole 18 only

    Args:
        hole_scores: List of 18 hole scores

    Returns:
        OCBScores object with all tiebreaker values
    """
    validate_hole_scores(hole_scores)

    return OCBScores(
        total=sum(hole_scores),
        last_9=sum(hole_scores[9:18]),   # Holes 10-18 (indices 9-17)
        last_6=sum(hole_scores[12:18]),  # Holes 13-18 (indices 12-17)
        last_3=sum(hole_scores[15:18]),  # Holes 16-18 (indices 15-17)
        last_hole=hole_scores[17]        # Hole 18 (index 17)
    )


def calculate_ocb_net(
    hole_scores: List[int],
    player_handicap: int,
    hole_stroke_indices: List[int]
) -> OCBScores:
    """
    Calculate OCB tiebreaker values for net scores.

    Legacy formulas (D1Nocb sheet):
        AO8 (Last9) = SUM(AF8:AN8)  # NET scores holes 10-18
        AP8 (Last6) = SUM(AI8:AN8)  # NET scores holes 13-18
        AQ8 (Last3) = SUM(AL8:AN8)  # NET scores holes 16-18
        AR8 (H18)   = AN8           # NET score hole 18

    Args:
        hole_scores: List of 18 gross hole scores
        player_handicap: Player's course handicap
        hole_stroke_indices: Stroke indices for each hole

    Returns:
        OCBScores object with net score tiebreaker values
    """
    validate_hole_scores(hole_scores)
    validate_handicap(player_handicap)
    validate_stroke_indices(hole_stroke_indices)

    # Calculate net scores for each hole
    net_scores = [
        calculate_net_hole_score(gross, player_handicap, idx)
        for gross, idx in zip(hole_scores, hole_stroke_indices)
    ]

    return OCBScores(
        total=sum(net_scores),
        last_9=sum(net_scores[9:18]),
        last_6=sum(net_scores[12:18]),
        last_3=sum(net_scores[15:18]),
        last_hole=net_scores[17]
    )


def rank_players(
    players: List[PlayerRoundScore],
    use_net_scores: bool = True
) -> List[PlayerRoundScore]:
    """
    Rank players by total score and OCB tiebreakers.

    Sorting priority (ascending - lower is better):
    1. Total Score
    2. Last 9 Holes
    3. Last 6 Holes
    4. Last 3 Holes
    5. Hole 18

    Args:
        players: List of PlayerRoundScore objects
        use_net_scores: If True, rank by net scores; else by gross

    Returns:
        Sorted list of players with 'rank' field populated
    """
    # Sort by OCB tuple
    players_sorted = sorted(
        players,
        key=lambda p: (
            p.ocb_net.as_tuple() if use_net_scores else p.ocb_gross.as_tuple()
        )
    )

    # Assign ranks (handle ties)
    current_rank = 1
    for i, player in enumerate(players_sorted):
        if i > 0:
            prev_player = players_sorted[i - 1]
            prev_ocb = prev_player.ocb_net if use_net_scores else prev_player.ocb_gross
            curr_ocb = player.ocb_net if use_net_scores else player.ocb_gross

            # Check if tied with previous player (all OCB values equal)
            if prev_ocb.as_tuple() == curr_ocb.as_tuple():
                # Tied - same rank as previous
                player.rank = prev_player.rank
            else:
                # Not tied - rank is current position
                player.rank = current_rank
        else:
            player.rank = 1

        current_rank += 1

    return players_sorted


def rank_players_by_division(
    players: List[PlayerRoundScore],
    division: str,
    use_net_scores: bool = True
) -> List[PlayerRoundScore]:
    """
    Rank players within a specific division.

    Args:
        players: All players
        division: Division name (e.g., 'Championship', 'A', 'B')
        use_net_scores: If True, rank by net scores; else by gross

    Returns:
        Ranked players in this division only
    """
    division_players = [p for p in players if p.division == division]
    ranked = rank_players(division_players, use_net_scores)

    # Set division ranks
    for i, player in enumerate(ranked, 1):
        player.rank_division = i

    return ranked


def calculate_multi_round_score(
    round_scores: List[OCBScores]
) -> OCBScores:
    """
    Calculate cumulative score and OCB for multiple rounds.

    For 36-hole and 54-hole tournaments.

    Args:
        round_scores: List of OCBScores for each round

    Returns:
        Combined OCBScores for all rounds
    """
    return OCBScores(
        total=sum(r.total for r in round_scores),
        last_9=sum(r.last_9 for r in round_scores),
        last_6=sum(r.last_6 for r in round_scores),
        last_3=sum(r.last_3 for r in round_scores),
        last_hole=round_scores[-1].last_hole  # Last hole of final round
    )
