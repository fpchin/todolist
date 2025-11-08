"""
Tournament models for GTMS.
"""
from django.db import models
from apps.core.models import TimeStampedModel


class Tournament(TimeStampedModel):
    """Tournament master data."""

    class TournamentFormat(models.TextChoices):
        STROKEPLAY = 'STROKEPLAY', 'Stroke Play'
        STABLEFORD = 'STABLEFORD', 'Stableford'
        MATCHPLAY = 'MATCHPLAY', 'Match Play'
        SCRAMBLE = 'SCRAMBLE', 'Scramble'

    class TournamentStatus(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        OPEN = 'OPEN', 'Open for Registration'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    format_type = models.CharField(
        max_length=20,
        choices=TournamentFormat.choices,
        default=TournamentFormat.STROKEPLAY
    )
    status = models.CharField(
        max_length=20,
        choices=TournamentStatus.choices,
        default=TournamentStatus.DRAFT
    )
    description = models.TextField(blank=True)
    max_players = models.IntegerField(default=200)

    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['-start_date', 'status']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.name} ({self.start_date})"


class TournamentPlayer(TimeStampedModel):
    """Junction table for tournament player registration."""

    class RegistrationStatus(models.TextChoices):
        REGISTERED = 'REGISTERED', 'Registered'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        WITHDRAWN = 'WITHDRAWN', 'Withdrawn'
        DISQUALIFIED = 'DISQUALIFIED', 'Disqualified'

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    player = models.ForeignKey(
        'players.Player',
        on_delete=models.CASCADE,
        related_name='tournament_registrations'
    )
    handicap_index = models.DecimalField(max_digits=4, decimal_places=1)
    playing_handicap = models.IntegerField()
    division = models.CharField(max_length=50)
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=RegistrationStatus.choices,
        default=RegistrationStatus.REGISTERED
    )

    class Meta:
        unique_together = [['tournament', 'player']]
        ordering = ['division', 'player__last_name']
        indexes = [
            models.Index(fields=['tournament', 'division']),
            models.Index(fields=['tournament', 'status']),
        ]

    def __str__(self):
        return f"{self.player.full_name} - {self.tournament.name}"


class Round(TimeStampedModel):
    """Tournament round."""

    class RoundStatus(models.TextChoices):
        SCHEDULED = 'SCHEDULED', 'Scheduled'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name='rounds'
    )
    round_number = models.IntegerField()
    round_date = models.DateField()
    course = models.ForeignKey(
        'courses.CourseConfiguration',
        on_delete=models.PROTECT,
        related_name='rounds'
    )
    status = models.CharField(
        max_length=20,
        choices=RoundStatus.choices,
        default=RoundStatus.SCHEDULED
    )

    class Meta:
        unique_together = [['tournament', 'round_number']]
        ordering = ['tournament', 'round_number']
        indexes = [
            models.Index(fields=['tournament', 'round_number']),
            models.Index(fields=['round_date']),
        ]

    def __str__(self):
        return f"{self.tournament.name} - Round {self.round_number}"


class TeeTime(TimeStampedModel):
    """Tee time (flight) assignment."""

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name='tee_times'
    )
    round = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        related_name='tee_times'
    )
    tee_time = models.DateTimeField()
    starting_hole = models.IntegerField(default=1)

    class Meta:
        ordering = ['round', 'tee_time']
        indexes = [
            models.Index(fields=['round', 'tee_time']),
        ]

    def __str__(self):
        return f"{self.round} - {self.tee_time.strftime('%H:%M')}"


class FlightPlayer(TimeStampedModel):
    """Players in a specific flight."""

    tee_time = models.ForeignKey(
        TeeTime,
        on_delete=models.CASCADE,
        related_name='players'
    )
    player = models.ForeignKey(
        'players.Player',
        on_delete=models.CASCADE,
        related_name='flight_assignments'
    )
    position = models.IntegerField()  # 1-4

    class Meta:
        unique_together = [
            ['tee_time', 'player'],
            ['tee_time', 'position']
        ]
        ordering = ['tee_time', 'position']

    def __str__(self):
        return f"{self.player.full_name} - {self.tee_time}"
