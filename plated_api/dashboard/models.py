from core.models import BaseModel
from django.db import models
from exams.models.exam import Exam
from users.models import Student


class Score(BaseModel):
    """a table to store exam scores of students"""

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="scores",
        related_query_name="score",
    )
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="scores",
        related_query_name="score",
    )
    score = models.IntegerField()
    duration = models.IntegerField()
    started_at = models.DateTimeField()

    class Meta:
        db_table = "scores"
        verbose_name = "Score"
        verbose_name_plural = "Scores"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.student} - {self.exam}"

    @property
    def max_score(self) -> int:
        return self.exam.questions.count()

    @property
    def percentage(self) -> int:
        return (self.score / self.max_score) * 100
