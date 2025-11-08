"""
Player models for GTMS.
"""
from django.db import models
from django.core.validators import EmailValidator
from apps.core.models import TimeStampedModel


class Player(TimeStampedModel):
    """Golf player master data."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(
        max_length=255,
        unique=True,
        validators=[EmailValidator()]
    )
    phone = models.CharField(max_length=20, blank=True)
    club_affiliation = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        """Return full name."""
        return f"{self.first_name} {self.last_name}"


class HandicapHistory(TimeStampedModel):
    """Historical handicap records for players."""

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='handicap_history'
    )
    handicap_index = models.DecimalField(max_digits=4, decimal_places=1)
    effective_date = models.DateField()
    issuing_authority = models.CharField(max_length=100)

    class Meta:
        ordering = ['player', '-effective_date']
        indexes = [
            models.Index(fields=['player', '-effective_date']),
        ]
        verbose_name_plural = 'Handicap histories'

    def __str__(self):
        return f"{self.player.full_name} - {self.handicap_index} ({self.effective_date})"
