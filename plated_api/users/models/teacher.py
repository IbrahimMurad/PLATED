""" This module defines teacher model for teachers table
"""

from core.models import BaseModel
from django.db import models
from resources.models import Subject
from users.models import User


class Teacher(BaseModel):
    """teacher model for teachers table"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher",
        related_query_name="teacher",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="teachers",
        related_query_name="teacher",
    )
    max_students = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "teachers"
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    def __str__(self):
        return self.user.username

    def get_full_name(self):
        return self.user.get_full_name()

    def get_short_name(self):
        return self.user.get_short_name()
