""" Unit model
"""

from django.db import models
from django.urls import reverse
from subjects.models.base import MaterialBaseModel
from curriculum.context_processors import CURRENT_SEMESTER
from .units import Unit


class RelevantChapterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(lesson__semester=CURRENT_SEMESTER)


class Chapter(MaterialBaseModel):
    """chapters table"""

    unit = models.ForeignKey(
        Unit,
        related_name="chapters",
        related_query_name="chapter",
        on_delete=models.CASCADE,
    )

    objects = models.Manager()
    relevant = RelevantChapterManager()

    def get_absolute_url(self):
        return reverse("lessons-list", kwargs={"pk": self.pk})

    @property
    def questions(self):
        from questions.models import Question

        return Question.objects.filter(lesson__chapter=self)
