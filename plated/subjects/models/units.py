""" Unit model
"""

from django.db import models
from django.urls import reverse
from subjects.models.base import MaterialBaseModel
from .subjects import Subject


class Unit(MaterialBaseModel):
    """ units table """
    subject = models.ForeignKey(Subject, related_name='units', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("chapters-list", kwargs={"pk": self.pk})
