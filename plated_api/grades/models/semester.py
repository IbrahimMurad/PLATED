"""this file contains the model for semesters table
"""

from datetime import date

from core.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class CurrentSemesterManager(models.Manager):
    """manager to get the currently running semester"""

    def get_queryset(self):
        """get the current semester"""
        return (
            super()
            .get_queryset()
            .filter(starts_at__lte=date.today(), ends_at__gte=date.today())
        )


class Semester(BaseModel):
    """semester model"""

    class SemesterChoices(models.TextChoices):
        """choices for semesters"""

        FIRST_TERM = "FIRST_TERM", _("First term")
        SECOND_TERM = "SECOND_TERM", _("Second term")
        No_TERM = "No_TERM", _("No term - Full year")
        SUMMER_COURSE = "SUMMER_COURSE", _("Summer course")

    name = models.CharField(
        max_length=255,
        choices=SemesterChoices.choices,
        default=SemesterChoices.FIRST_TERM,
    )
    starts_at = models.DateField(default=date(year=2024, month=9, day=1))
    ends_at = models.DateField(default=date(year=2024, month=12, day=31))

    objects = models.Manager()
    current = CurrentSemesterManager()

    class Meta:
        db_table = "semesters"

    def __str__(self) -> str:
        return self.name
