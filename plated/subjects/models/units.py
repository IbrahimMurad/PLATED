""" Unit model
"""

from django.db import models
from subjects.models.base import MaterialBaseModel
from .subjects import Subject


class Unit(MaterialBaseModel):
    """ units table """
    subject = models.ForeignKey(Subject, related_name='units', on_delete=models.CASCADE)
