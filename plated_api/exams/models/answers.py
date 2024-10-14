from core.models import BaseModel
from django.db import models
from exams.models.exam import Exam
from questions.models import Choice
from users.models import Student


class Answer(BaseModel):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        indexes = [
            models.Index(fields=["exam", "student"]),
        ]
        unique_together = [
            ["exam", "student", "choice"],
        ]
