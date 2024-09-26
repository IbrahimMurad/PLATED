from django.db import models

from core.models import BaseModel
from subjects.models import Lesson


class Question(BaseModel):
    """questions table"""

    body = models.TextField()
    difficulty = models.SmallIntegerField(
        choices=[(1, "Easy"), (2, "Medium"), (3, "Hard"), (4, "Very Hard")]
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="questions",
        related_query_name="question",
    )
    graph = models.ImageField(upload_to="questions_graphs/", null=True, blank=True)

    def __str__(self):
        return self.body[:50]

    class Meta:
        ordering = ["?"]


class Answer(BaseModel):
    """answers table"""

    body = models.CharField(max_length=256, null=True, blank=True)
    graph = models.ImageField(upload_to="answers_graphs/", null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )

    def __str__(self):
        return self.body
