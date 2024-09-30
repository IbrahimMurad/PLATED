"""this file contains the model for the grades table
"""

from core.models import BaseModel
from django.db import models
from grades.models.stage import Stage


class Grade(BaseModel):
    """grade model"""

    stage = models.ForeignKey(
        to=Stage,
        on_delete=models.CASCADE,
        related_name="grades",
        related_query_name="grade",
    )
    name = models.CharField(max_length=255)
    order_in_stage = models.PositiveIntegerField()

    class Meta:
        db_table = "grades"
        ordering = ["order_in_stage"]

    def __str__(self) -> str:
        return f"{self.name} - {self.stage}"
