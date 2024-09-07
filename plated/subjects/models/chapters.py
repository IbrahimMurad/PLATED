""" Unit model
"""

from django.db import models
from subjects.models.base import MaterialBaseModel
from .units import Unit


class Chapter(MaterialBaseModel):
    """ chapters table """
    unit = models.ForeignKey(Unit, related_name='chapters', on_delete=models.CASCADE)
