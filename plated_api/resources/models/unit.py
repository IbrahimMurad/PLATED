""" This file is to define a model for the units of the textbooks. """

from django.db import models
from resources.models import ResourceBase, TextBook


class Unit(ResourceBase):
    """unit model for units table."""

    textBook = models.ForeignKey(TextBook, on_delete=models.CASCADE)

    class Meta:
        db_table = "units"
