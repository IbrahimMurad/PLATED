"""this file contains the model for the stages table
"""

from core.models import BaseModel
from django.db import models
from grades.models.path import Path


class Stage(BaseModel):
    """stage model"""

    path = models.ForeignKey(
        to=Path,
        on_delete=models.CASCADE,
        related_name="stages",
        related_query_name="stage",
    )
    name = models.CharField(max_length=255)
    order_in_path = models.PositiveIntegerField()

    class Meta:
        db_table = "stages"
        ordering = ["order_in_path"]

    def __str__(self) -> str:
        return f"{self.name} - {self.path}"
