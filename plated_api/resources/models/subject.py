""" This file is to define a model for the subject. """

from core.models import BaseModel
from django.db import models


class Subject(BaseModel):
    """subject model to hold only the name of the subject, more like a category."""

    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        help_text="Subject name (case-insensitive).",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]
        db_table = "subjects"
