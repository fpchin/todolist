"""
Unit tests for the scoring calculation engine.

Tests are based on the legacy system formulas extracted from:
21ST SIBU AMATEUR OPEN GOLF CHAMPIONSHIP 2023.xlsm
"""
import pytest
from apps.scoring.engine import (
    calculate_gross_score,
    calculate_net_hole_score,
    calculate_net_score,
    get_strokes_received_per_hole,
    calculate_ocb_gross,
    calculate_ocb_net,
    rank_players,
    rank_players_by_division,
    calculate_multi_round_score,
)
from apps.scoring.models import OCBScores, PlayerRoundScore
from apps.scoring.exceptions import (
    InvalidHoleCountError,
    InvalidScoreError,
    InvalidHandicapError,
    InvalidStrokeIndexError,
)


# Standard stroke indices (typical golf course)
STANDARD_STROKE_INDICES = [5, 3, 17, 9, 1, 11, 15, 7, 13, 4, 10, 2, 18, 14, 6, 12, 16, 8]


class TestGrossScoreCalculation:
    """Test gross score calculations."""

    def test_calculate_gross_score_valid(self):
        """Test gross score calculation with valid inputs."""
        hole_scores = [4, 5, 3, 4, 5, 4, 3, 5, 4, 4, 4, 5, 3, 4, 5, 4, 4, 5]
        result = calculate_gross_score(hole_scores)
        assert result == 75

    def test_calculate_gross_score_par(self):
        """Test gross score for a par round (all 4s)."""
        hole_scores = [4] * 18
        result = calculate_gross_score(hole_scores)
        assert result == 72

    def test_calculate_gross_score_invalid_count(self):
        """Test that invalid hole count raises error."""
        hole_scores = [4, 5, 3]  # Only 3 holes
        with pytest.raises(InvalidHoleCountError):
            calculate_gross_score(hole_scores)

    def test_calculate_gross_score_invalid_score(self):
        """Test that invalid score raises error."""
        hole_scores = [4, 5, 3, 4, 5, 4, 3, 5, 4, 4, 4, 5, 3, 4, 5, 4, 4, 0]  # Last hole = 0
        with pytest.raises(InvalidScoreError):
            calculate_gross_score(hole_scores)

    def test_calculate_gross_score_too_high(self):
        """Test that too high score raises error."""
        hole_scores = [4, 5, 3, 4, 5, 4, 3, 5, 4, 4, 4, 5, 3, 4, 5, 4, 4, 20]  # Last hole = 20
        with pytest.raises(InvalidScoreError):
            calculate_gross_score(hole_scores)


class TestNetScoreCalculation:
    """Test net score calculations."""

    def test_net_hole_score_no_stroke(self):
        """Test net score when no stroke is received."""
        result = calculate_net_hole_score(
            gross_hole_score=4,
            player_handicap=5,
            hole_stroke_index=10  # Handicap 5 < Index 10, no stroke
        )
        assert result == 4

    def test_net_hole_score_with_stroke(self):
        """Test net score when stroke is received."""
        result = calculate_net_hole_score(
            gross_hole_score=5,
            player_handicap=12,
            hole_stroke_index=8  # Handicap 12 >= Index 8, receive stroke
        )
        assert result == 4

    def test_calculate_net_score_scratch_golfer(self):
        """Test net score for scratch golfer (handicap 0)."""
        hole_scores = [4, 5, 3, 4, 5, 4, 3, 5, 4, 4, 4, 5, 3, 4, 5, 4, 4, 5]
        result = calculate_net_score(hole_scores, 0, STANDARD_STROKE_INDICES)
        assert result == 75  # Same as gross

    def test_calculate_net_score_18_handicap(self):
        """Test net score for 18 handicap player."""
        hole_scores = [5, 6, 4, 5, 6, 5, 4, 6, 5, 5, 5, 6, 4, 5, 6, 5, 5, 6]
        gross = sum(hole_scores)
        assert gross == 93

        result = calculate_net_score(hole_scores, 18, STANDARD_STROKE_INDICES)
        assert result == 75  # 93 - 18 = 75

    def test_calculate_net_score_9_handicap(self):
        """Test net score for 9 handicap player."""
        hole_scores = [5, 6, 4, 5, 6, 5, 4, 6, 5, 5, 5, 6, 4, 5, 6, 5, 5, 6]
        gross = sum(hole_scores)
        assert gross == 93

        # Should receive strokes on holes with index 1-9 only
        result = calculate_net_score(hole_scores, 9, STANDARD_STROKE_INDICES)
        assert result == 84  # 93 - 9 = 84


class TestStrokeAllocation:
    """Test handicap stroke allocation."""

    def test_strokes_received_zero_handicap(self):
        """Test stroke allocation for scratch golfer."""
        strokes = get_strokes_received_per_hole(0, STANDARD_STROKE_INDICES)
        assert strokes == [0] * 18

    def test_strokes_received_18_handicap(self):
        """Test stroke allocation for 18 handicap."""
        strokes = get_strokes_received_per_hole(18, STANDARD_STROKE_INDICES)
        assert strokes == [1] * 18
        assert sum(strokes) == 18

    def test_strokes_received_9_handicap(self):
        """Test stroke allocation for 9 handicap."""
        strokes = get_strokes_received_per_hole(9, STANDARD_STROKE_INDICES)
        # Should get strokes on holes with index 1-9
        for i, idx in enumerate(STANDARD_STROKE_INDICES):
            if idx <= 9:
                assert strokes[i] == 1
            else:
                assert strokes[i] == 0
        assert sum(strokes) == 9

    def test_strokes_received_24_handicap(self):
        """Test stroke allocation for 24 handicap (>18)."""
        strokes = get_strokes_received_per_hole(24, STANDARD_STROKE_INDICES)
        # Should get 1 stroke on all 18 + extra stroke on index 1-6
        for i, idx in enumerate(STANDARD_STROKE_INDICES):
            if idx <= 6:
                assert strokes[i] == 2  # Two strokes
            else:
                assert strokes[i] == 1  # One stroke
        assert sum(strokes) == 24

    def test_strokes_received_36_handicap(self):
        """Test stroke allocation for 36 handicap (2 full cycles)."""
        strokes = get_strokes_received_per_hole(36, STANDARD_STROKE_INDICES)
        assert strokes == [2] * 18
        assert sum(strokes) == 36

    def test_invalid_handicap_negative(self):
        """Test that negative handicap raises error."""
        with pytest.raises(InvalidHandicapError):
            get_strokes_received_per_hole(-1, STANDARD_STROKE_INDICES)

    def test_invalid_handicap_too_high(self):
        """Test that too high handicap raises error."""
        with pytest.raises(InvalidHandicapError):
            get_strokes_received_per_hole(55, STANDARD_STROKE_INDICES)


class TestOCBCalculations:
    """Test OCB (Order of Card Back) tiebreaker calculations."""

    def test_ocb_gross_calculation(self):
        """Test OCB gross score calculation."""
        hole_scores = [4, 5, 3, 4, 5, 4, 3, 5, 4, 4, 4, 5, 3, 4, 5, 4, 4, 5]
        ocb = calculate_ocb_gross(hole_scores)

        assert ocb.total == 75
        assert ocb.last_9 == sum(hole_scores[9:18])  # Holes 10-18
        assert ocb.last_6 == sum(hole_scores[12:18])  # Holes 13-18
        assert ocb.last_3 == sum(hole_scores[15:18])  # Holes 16-18
        assert ocb.last_hole == hole_scores[17]  # Hole 18

    def test_ocb_net_calculation(self):
        """Test OCB net score calculation."""
        hole_scores = [5, 6, 4, 5, 6, 5, 4, 6, 5, 5, 5, 6, 4, 5, 6, 5, 5, 6]
        player_handicap = 18

        ocb = calculate_ocb_net(hole_scores, player_handicap, STANDARD_STROKE_INDICES)

        # Each hole gets -1 stroke for 18 handicap
        expected_net_scores = [s - 1 for s in hole_scores]

        assert ocb.total == sum(expected_net_scores)
        assert ocb.last_9 == sum(expected_net_scores[9:18])
        assert ocb.last_6 == sum(expected_net_scores[12:18])
        assert ocb.last_3 == sum(expected_net_scores[15:18])
        assert ocb.last_hole == expected_net_scores[17]

    def test_ocb_as_tuple(self):
        """Test OCB as_tuple method for sorting."""
        ocb = OCBScores(75, 38, 25, 13, 5)
        assert ocb.as_tuple() == (75, 38, 25, 13, 5)


class TestPlayerRanking:
    """Test player ranking with OCB tiebreakers."""

    def create_player(
        self,
        player_id: str,
        name: str,
        division: str,
        hole_scores: list,
        handicap: int
    ) -> PlayerRoundScore:
        """Helper to create a player score object."""
        gross = calculate_gross_score(hole_scores)
        net = calculate_net_score(hole_scores, handicap, STANDARD_STROKE_INDICES)
        ocb_gross = calculate_ocb_gross(hole_scores)
        ocb_net = calculate_ocb_net(hole_scores, handicap, STANDARD_STROKE_INDICES)

        return PlayerRoundScore(
            player_id=player_id,
            player_name=name,
            handicap=handicap,
            division=division,
            hole_scores=hole_scores,
            gross_score=gross,
            net_score=net,
            ocb_gross=ocb_gross,
            ocb_net=ocb_net
        )

    def test_ranking_simple(self):
        """Test simple ranking without ties."""
        player1 = self.create_player(
            "P1", "John", "A",
            [4, 5, 3, 4, 5, 4, 3, 5, 4, 4, 4, 5, 3, 4, 5, 4, 4, 5],  # Net 75
            0
        )
        player2 = self.create_player(
            "P2", "Jane", "A",
            [5, 6, 4, 5, 6, 5, 4, 6, 5, 5, 5, 6, 4, 5, 6, 5, 5, 6],  # Net 75
            18
        )
        player3 = self.create_player(
            "P3", "Bob", "A",
            [5, 6, 5, 5, 6, 5, 5, 6, 5, 5, 5, 6, 5, 5, 6, 5, 5, 7],  # Net 77
            18
        )

        players = [player3, player1, player2]  # Out of order
        ranked = rank_players(players, use_net_scores=True)

        # Both player1 and player2 have net 75, player3 has net 77
        assert ranked[0].rank == 1
        assert ranked[1].rank == 1  # Tied
        assert ranked[2].rank == 3  # Rank 3 (not 2) because two players ahead

    def test_ranking_with_ocb_tiebreaker(self):
        """Test ranking with OCB tiebreaker."""
        # Both players net 75, but different back-nine scores
        player1 = self.create_player(
            "P1", "John", "A",
            # Front 9: 43, Back 9: 32 (better)
            [5, 5, 4, 5, 5, 5, 4, 5, 5, 4, 4, 3, 3, 4, 4, 3, 3, 4],
            18
        )
        player2 = self.create_player(
            "P2", "Jane", "A",
            # Front 9: 41, Back 9: 34 (worse)
            [4, 4, 5, 4, 5, 4, 5, 5, 5, 5, 5, 4, 4, 5, 5, 4, 4, 5],
            18
        )

        players = [player2, player1]  # Out of order
        ranked = rank_players(players, use_net_scores=True)

        # Both net 75, but player1 wins on last_9
        assert ranked[0].player_id == "P1"
        assert ranked[0].rank == 1
        assert ranked[1].player_id == "P2"
        assert ranked[1].rank == 2

    def test_ranking_by_division(self):
        """Test ranking players by division."""
        player_a1 = self.create_player("PA1", "John", "A", [4]*18, 0)
        player_a2 = self.create_player("PA2", "Jane", "A", [5]*18, 0)
        player_b1 = self.create_player("PB1", "Bob", "B", [4]*18, 10)
        player_b2 = self.create_player("PB2", "Alice", "B", [6]*18, 10)

        all_players = [player_a2, player_b2, player_a1, player_b1]

        # Rank division A
        div_a = rank_players_by_division(all_players, "A", use_net_scores=True)
        assert len(div_a) == 2
        assert div_a[0].player_id == "PA1"
        assert div_a[0].rank_division == 1
        assert div_a[1].player_id == "PA2"
        assert div_a[1].rank_division == 2

        # Rank division B
        div_b = rank_players_by_division(all_players, "B", use_net_scores=True)
        assert len(div_b) == 2
        assert div_b[0].player_id == "PB1"
        assert div_b[0].rank_division == 1


class TestMultiRoundCalculations:
    """Test multi-round (36-hole, 54-hole) calculations."""

    def test_calculate_multi_round_36_hole(self):
        """Test 36-hole cumulative score."""
        round1 = OCBScores(total=75, last_9=38, last_6=25, last_3=13, last_hole=5)
        round2 = OCBScores(total=77, last_9=40, last_6=27, last_3=14, last_hole=6)

        combined = calculate_multi_round_score([round1, round2])

        assert combined.total == 152  # 75 + 77
        assert combined.last_9 == 78  # 38 + 40
        assert combined.last_6 == 52  # 25 + 27
        assert combined.last_3 == 27  # 13 + 14
        assert combined.last_hole == 6  # Last hole of final round

    def test_calculate_multi_round_54_hole(self):
        """Test 54-hole cumulative score."""
        round1 = OCBScores(75, 38, 25, 13, 5)
        round2 = OCBScores(77, 40, 27, 14, 6)
        round3 = OCBScores(76, 39, 26, 13, 5)

        combined = calculate_multi_round_score([round1, round2, round3])

        assert combined.total == 228  # 75 + 77 + 76
        assert combined.last_9 == 117  # 38 + 40 + 39
        assert combined.last_6 == 78  # 25 + 27 + 26
        assert combined.last_3 == 40  # 13 + 14 + 13
        assert combined.last_hole == 5  # Last hole of round 3


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_perfect_round_all_ones(self):
        """Test theoretical perfect round (hole-in-one on every hole)."""
        hole_scores = [1] * 18
        gross = calculate_gross_score(hole_scores)
        assert gross == 18

    def test_maximum_score_all_fifteens(self):
        """Test maximum allowed score."""
        hole_scores = [15] * 18
        gross = calculate_gross_score(hole_scores)
        assert gross == 270

    def test_zero_handicap_net_equals_gross(self):
        """Test that net score equals gross for scratch golfer."""
        hole_scores = [4, 5, 3, 4, 5, 4, 3, 5, 4, 4, 4, 5, 3, 4, 5, 4, 4, 5]
        gross = calculate_gross_score(hole_scores)
        net = calculate_net_score(hole_scores, 0, STANDARD_STROKE_INDICES)
        assert gross == net

    def test_invalid_stroke_indices_duplicate(self):
        """Test that duplicate stroke indices raise error."""
        invalid_indices = [1, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        with pytest.raises(InvalidStrokeIndexError):
            get_strokes_received_per_hole(18, invalid_indices)

    def test_invalid_stroke_indices_wrong_count(self):
        """Test that wrong number of indices raises error."""
        invalid_indices = [1, 2, 3]  # Only 3
        with pytest.raises(InvalidStrokeIndexError):
            get_strokes_received_per_hole(18, invalid_indices)
