""" This module defines a custom user model for this project
"""

from core.models import BaseModel
from django.db import models
from grades.models import Grade
from users.models import User


class Student(BaseModel):
    """student model for students table"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student",
        related_query_name="student",
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.PROTECT,
        related_name="students",
        related_query_name="student",
    )

    class Meta:
        db_table = "students"
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self) -> str:
        return self.user.username

    def get_full_name(self) -> str:
        return self.user.get_full_name()

    def get_short_name(self) -> str:
        return self.user.get_short_name()
