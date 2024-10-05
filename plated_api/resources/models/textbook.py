""" This file is to define a model for the textbooks. """

from django.db import models
from resources.models import ResourceBase, Subject


class TextBook(ResourceBase):
    """textbook model for different textbooks required for the student."""

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    order_index = None  # type: ignore

    class Meta:
        ordering = ["title"]
        db_table = "textbooks"
