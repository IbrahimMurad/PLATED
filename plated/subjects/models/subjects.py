""" Subject model
"""

from subjects.models.base import MaterialBaseModel
from django.db import models
from curriculum.models import Grade


class Subject(MaterialBaseModel):
    """ subjects table """
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        related_name='subjects',
        related_query_name='subject',
        default=Grade.objects.first().id
        )
    order_in_syllabus = None
    number = None
    
    class Meta:
        ordering = ['title']
