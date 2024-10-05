""" This file is to define a model for the units of the textbooks. """

from django.db import models
from resources.models import ResourceBase


class Chapter(ResourceBase):
    """chapter model for chapters table."""

    unit = models.ForeignKey("Unit", on_delete=models.CASCADE)

    class Meta:
        db_table = "chapters"
