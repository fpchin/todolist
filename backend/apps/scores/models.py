"""
Score and result models for GTMS.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel


class HoleScore(TimeStampedModel):
    """Individual hole score with detailed statistics."""

    round = models.ForeignKey(
        'tournaments.Round',
        on_delete=models.CASCADE,
        related_name='hole_scores'
    )
    player = models.ForeignKey(
        'players.Player',
        on_delete=models.CASCADE,
        related_name='hole_scores'
    )
    hole_number = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(18)
        ]
    )
    strokes = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(20)
        ]
    )
    putts = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
    fairway_hit = models.BooleanField(null=True, blank=True)
    green_in_regulation = models.BooleanField(null=True, blank=True)
    penalty_strokes = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
    verified = models.BooleanField(default=False)
    scorer = models.ForeignKey(
        'players.Player',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='scores_entered'
    )

    class Meta:
        unique_together = [['round', 'player', 'hole_number']]
        ordering = ['round', 'player', 'hole_number']
        indexes = [
            models.Index(fields=['round', 'player', 'hole_number']),
            models.Index(fields=['round', 'player']),
            models.Index(fields=['verified'], condition=models.Q(verified=False)),
        ]

    def __str__(self):
        return f"{self.player.full_name} - {self.round} - Hole {self.hole_number}: {self.strokes}"


class Result(TimeStampedModel):
    """Calculated tournament results and rankings."""

    tournament = models.ForeignKey(
        'tournaments.Tournament',
        on_delete=models.CASCADE,
        related_name='results'
    )
    player = models.ForeignKey(
        'players.Player',
        on_delete=models.CASCADE,
        related_name='tournament_results'
    )
    division = models.CharField(max_length=50)
    total_gross = models.IntegerField(validators=[MinValueValidator(0)])
    total_net = models.IntegerField(validators=[MinValueValidator(0)])
    total_points = models.IntegerField(null=True, blank=True)  # For Stableford

    # OCB (Order of Card Back) tiebreaker values
    gross_last_9 = models.IntegerField(default=0)
    gross_last_6 = models.IntegerField(default=0)
    gross_last_3 = models.IntegerField(default=0)
    gross_last_hole = models.IntegerField(default=0)

    net_last_9 = models.IntegerField(default=0)
    net_last_6 = models.IntegerField(default=0)
    net_last_3 = models.IntegerField(default=0)
    net_last_hole = models.IntegerField(default=0)

    rank_overall = models.IntegerField(validators=[MinValueValidator(1)])
    rank_division = models.IntegerField(validators=[MinValueValidator(1)])
    prize_category = models.CharField(max_length=100, blank=True)
    calculated_at = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)

    class Meta:
        unique_together = [['tournament', 'player']]
        ordering = ['tournament', 'rank_overall']
        indexes = [
            models.Index(fields=['tournament', 'rank_overall']),
            models.Index(fields=['tournament', 'division', 'rank_division']),
        ]

    def __str__(self):
        return f"{self.player.full_name} - {self.tournament.name} - Rank {self.rank_overall}"
