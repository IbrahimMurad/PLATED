""" Unit model
"""

from django.db import models
from django.urls import reverse
from subjects.models.base import MaterialBaseModel
from .units import Unit


class Chapter(MaterialBaseModel):
    """ chapters table """
    unit = models.ForeignKey(Unit, related_name='chapters', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("lessons-list", kwargs={"pk": self.pk})
