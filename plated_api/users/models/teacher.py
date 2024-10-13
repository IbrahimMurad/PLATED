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
    max_students = models.PositiveIntegerField(default=10)

    class Meta:
        db_table = "teachers"
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    def __str__(self) -> str:
        return self.user.username

    def get_full_name(self) -> str:
        return self.user.get_full_name()

    def get_short_name(self) -> str:
        return self.user.get_short_name()

    @property
    def available_students(self) -> int:
        return (
            self.max_students
            - self.classes.aggregate(models.Sum("students_count"))[
                "students_count__sum"
            ]
            or 0
        )
