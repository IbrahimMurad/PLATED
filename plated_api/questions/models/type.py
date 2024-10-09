""" This file defines Type model under which questions will be categorized
"""

from core.models import BaseModel
from django.db import models
from resources.models import Subject


class Type(BaseModel):
    """Type model for types table"""

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="types",
        related_query_name="type",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=128)

    class Meta:
        db_table = "types"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
