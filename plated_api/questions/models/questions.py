""" This file defines Question model in which questions will be stored
with their respective types and detailed solution.
Also, it links the Question model with its scoped lesson.
It contains the QuestionManager class which will be used to filter out questions
based on their types.
"""

from core.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from questions.models.type import Type
from resources.models import Lesson


def question_figure_path(instance, filename: str) -> str:
    """Return the path to store question figure"""
    return f"questions/{instance.id}/figures/{filename}"


class Question(BaseModel):
    """Question model for questions table"""

    class Difficulty(models.TextChoices):
        """Difficulty choices for questions"""

        EASY: tuple = "easy", _("Easy")
        MEDIUM: tuple = "medium", _("Medium")
        HARD: tuple = "hard", _("Hard")
        VERY_HARD: tuple = "very hard", _("Very Hard")

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="questions",
        related_query_name="question",
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name="questions",
        related_query_name="question",
    )
    difficulty = models.CharField(
        max_length=32, choices=Difficulty.choices, default=Difficulty.EASY
    )
    body = models.TextField()
    solution = models.TextField(
        null=True, blank=True, help_text="Detailed solution (soluation manual)"
    )
    figure = models.ImageField(
        upload_to=question_figure_path,
        null=True,
        blank=True,
        help_text="Question figure (diagram, graph, etc.)",
    )

    class Meta:
        db_table = "questions"
        ordering = ["?"]

    def __str__(self) -> str:
        return self.body[:50]
