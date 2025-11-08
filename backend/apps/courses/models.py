"""
Course configuration models for GTMS.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel


class CourseConfiguration(TimeStampedModel):
    """Golf course configuration."""

    course_name = models.CharField(max_length=255)
    tee_color = models.CharField(max_length=50)
    rating = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[
            MinValueValidator(60.0),
            MaxValueValidator(85.0)
        ]
    )
    slope = models.IntegerField(
        validators=[
            MinValueValidator(55),
            MaxValueValidator(155)
        ]
    )
    par = models.IntegerField(
        validators=[
            MinValueValidator(27),
            MaxValueValidator(90)
        ]
    )

    class Meta:
        ordering = ['course_name', 'tee_color']
        indexes = [
            models.Index(fields=['course_name', 'tee_color']),
        ]

    def __str__(self):
        return f"{self.course_name} ({self.tee_color}) - Par {self.par}"

    @property
    def stroke_indices(self):
        """Return list of stroke indices for all holes."""
        holes = self.holes.order_by('hole_number')
        return [hole.handicap_stroke_index for hole in holes]


class HoleConfiguration(TimeStampedModel):
    """Individual hole configuration."""

    course = models.ForeignKey(
        CourseConfiguration,
        on_delete=models.CASCADE,
        related_name='holes'
    )
    hole_number = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(18)
        ]
    )
    par = models.IntegerField(
        validators=[
            MinValueValidator(3),
            MaxValueValidator(5)
        ]
    )
    handicap_stroke_index = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(18)
        ]
    )
    distance = models.IntegerField(
        validators=[MinValueValidator(0)]
    )

    class Meta:
        unique_together = [['course', 'hole_number']]
        ordering = ['course', 'hole_number']
        indexes = [
            models.Index(fields=['course', 'hole_number']),
        ]

    def __str__(self):
        return f"{self.course.course_name} - Hole {self.hole_number} (Par {self.par})"
