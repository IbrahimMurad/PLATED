""" This file is to define a model for the units of the textbooks. """

from django.db import models
from resources.models import ResourceBase, TextBook


class Unit(ResourceBase):
    """unit model for units table."""

    text_book = models.ForeignKey(
        TextBook,
        on_delete=models.CASCADE,
        related_name="units",
        related_query_name="unit",
    )

    class Meta:
        db_table = "units"
        constraints = [
            models.UniqueConstraint(
                fields=["text_book", "syllabus_order"],
                name="unique_text_book_order",
            )
        ]
