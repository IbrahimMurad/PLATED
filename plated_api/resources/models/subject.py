""" This file is to define a model for the subject. """

from django.db import models


class Subject(models.Model):
    """subject model to hold only the name of the subject, more like a category."""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]
        db_table = "subjects"
