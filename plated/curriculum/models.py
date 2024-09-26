from django.db import models

from core.models import BaseModel


class Curriculum(BaseModel):
    """curriculums table"""

    name = models.CharField(max_length=32, default="arabic")

    def __str__(self):
        return f"{self.name}"


class Grade(BaseModel):
    """grades table"""

    title = models.CharField(max_length=64)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.curriculum}"


class Semester(BaseModel):
    """semesters table"""

    title = models.CharField(
        max_length=1,
        choices=[
            (
                "0",
                "No term",
            ),  # for grades with one term like third year of secondary school
            ("1", "first term"),
            ("2", "second term"),
        ],
    )
    starting_date = models.DateField()
    ending_date = models.DateField()

    def __str__(self):
        return f"{self.title}"
