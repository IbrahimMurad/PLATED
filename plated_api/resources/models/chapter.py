""" This file is to define a model for the units of the textbooks. """

from django.db import models
from resources.models import ResourceBase


class Chapter(ResourceBase):
    """chapter model for chapters table."""

    unit = models.ForeignKey(
        "Unit",
        on_delete=models.CASCADE,
        related_name="chapters",
        related_query_name="chapter",
    )

    class Meta:
        db_table = "chapters"
        constraints = [
            models.UniqueConstraint(
                fields=["unit", "syllabus_order"],
                name="unique_unit_order",
            )
        ]
