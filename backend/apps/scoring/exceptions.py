"""
Custom exceptions for the scoring engine.
"""


class ScoringError(Exception):
    """Base exception for scoring errors."""
    pass


class InvalidHoleCountError(ScoringError):
    """Raised when hole count != 18."""
    pass


class InvalidScoreError(ScoringError):
    """Raised when score is out of valid range."""
    pass


class InvalidHandicapError(ScoringError):
    """Raised when handicap is out of valid range."""
    pass


class InvalidStrokeIndexError(ScoringError):
    """Raised when stroke index is invalid."""
    pass
