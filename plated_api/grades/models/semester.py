"""this file contains the model for semesters table
"""

from datetime import date

from core.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from grades.models import Curriculum


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
    curriculum = models.ForeignKey(
        Curriculum,
        on_delete=models.CASCADE,
        related_name="semesters",
        related_query_name="semester",
        null=True,
        blank=True,
    )

    objects = models.Manager()
    current = CurrentSemesterManager()

    class Meta:
        db_table = "semesters"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.starts_at > self.ends_at:
            raise ValueError("starts_at should be less than ends_at")
        # check if there is already a current semester
        # the first condition checks for existing current semester
        # the second condition is for update save
        # the third condiction is for new non-current semester
        current_semester = Semester.current.filter(curriculum=self.curriculum)
        if (
            len(current_semester) >= 1
            and current_semester[0].id != self.id
            and self.starts_at <= date.today() <= self.ends_at
        ):
            raise ValueError("There should be only one current semester")
        super().save(*args, **kwargs)
