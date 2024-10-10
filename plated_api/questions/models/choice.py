""" This file defines Choice model in which choices of a question will be stored.
It links the Choice model with its scoped question,
acting as the choices of a multiple choice question.
"""

from typing import Optional

from core.models import BaseModel
from django.core.exceptions import ValidationError
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
            ),
            models.UniqueConstraint(
                fields=["question", "is_correct"],
                condition=models.Q(is_correct=True),
                name="unique_correct_choice",
            ),
        ]

    def clean(self) -> None:
        super().clean()
        if self.body and self.figure:
            raise ValidationError(
                "Choice can have either body or figure, not both, not neighter."
            )

        choices: models.QuerySet = self.question.choices.all()
        if choices.count() >= 4 and self not in choices:
            raise ValidationError("A question cannot have more than 4 choices.")

        if choices.exists():
            first_choice: Optional[Choice] = choices.first()
            if first_choice.body and self.figure:  # type: ignore
                raise ValidationError(
                    "All choices for a question must be of the same type"
                    " (text or figure)."
                )
            if first_choice.figure and self.body:  # type: ignore
                raise ValidationError(
                    "All choices for a question must be of the same type"
                    " (text or figure)."
                )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.body or self.figure.name
