from typing import Any

from core.models import BaseModel
from django.core.exceptions import ValidationError
from django.db import models
from users.models import Student, Teacher


class WithCount(models.Manager):
    def get_queryset(self) -> Any:
        return super().get_queryset().annotate(students_count=models.Count("students"))


class Class(BaseModel):
    """Class model for classes table"""

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="classes",
        related_query_name="class",
    )
    name = models.CharField("The name of the class", max_length=128)
    description = models.TextField(
        "The description of the class", blank=True, null=True
    )
    grade = models.ForeignKey(
        "grades.Grade",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="classes",
        related_query_name="class",
    )
    students = models.ManyToManyField(
        Student,
        related_name="classes",
        related_query_name="class",
    )

    objects = WithCount()

    class Meta:
        db_table = "classes"
        verbose_name = "Class"
        verbose_name_plural = "Classes"

    def clean(self, *args, **kwargs) -> None:
        """validate that all students are in the same grade as the class"""
        grade = self.students.values("grade").distinct()
        if len(grade) > 1:
            raise ValidationError("All students must be in the same grade")
        if not self.students and grade.first() != self.grade:
            raise ValidationError("All students must be in the same grade as the class")
        super().clean(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    @property
    def students_count(self) -> int:
        return self.students.count()
