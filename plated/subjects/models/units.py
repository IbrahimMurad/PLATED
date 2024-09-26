""" Unit model
"""

from django.db import models
from django.urls import reverse
from subjects.models.base import MaterialBaseModel
from .subjects import Subject
from curriculum.context_processors import CURRENT_SEMESTER


class RelevantUnitManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(chapter__lesson__semester=CURRENT_SEMESTER)


class Unit(MaterialBaseModel):
    """units table"""

    subject = models.ForeignKey(
        Subject,
        related_name="units",
        related_query_name="unit",
        on_delete=models.CASCADE,
    )

    objects = models.Manager()
    relevant = RelevantUnitManager()

    def get_absolute_url(self):
        return reverse("chapters-list", kwargs={"pk": self.pk})

    @property
    def questions(self):
        from questions.models import Question

        return Question.objects.filter(lesson__chapter__unit=self)
