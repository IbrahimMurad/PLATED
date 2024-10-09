""" This file defines Choice model in which choices of a question will be stored.
It links the Choice model with its scoped question,
acting as the choices of a multiple choice question.
"""

from core.models import BaseModel
from django.db import models
from questions.models.questions import Question


def choice_figure_path(instance, filename: str) -> str:
    """Return the path to store choice figure"""
    return f"questions/{instance.question.id}/choices/{instance.id}"


class Choice(BaseModel):
    """Choice model for choices table"""

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices",
        related_query_name="choice",
    )
    body = models.TextField(null=True, blank=True)
    figure = models.ImageField(
        upload_to=choice_figure_path,
        null=True,
        blank=True,
        help_text="Choice figure (diagram, graph, etc.)",
    )
    is_correct = models.BooleanField(default=False)

    class Meta:
        db_table = "choices"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(body__isnull=False) | models.Q(figure__isnull=False),
                name="body_figure_not_null",
            )
        ]

    def __str__(self) -> str:
        return self.body or self.figure.name
