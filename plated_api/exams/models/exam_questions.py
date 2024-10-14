from django.db import models
from exams.models.exam import Exam
from questions.models import Question


class ExamQuestions(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="exam_questions",
        related_query_name="exam_question",
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="exam_questions",
        related_query_name="exam_question",
    )
    order = models.IntegerField()

    class Meta:
        verbose_name = "Exam Question"
        verbose_name_plural = "Exam Questions"
        indexes = [
            models.Index(fields=["exam"]),
        ]
        unique_together = [
            ["exam", "question"],
        ]
        ordering = ["order"]
