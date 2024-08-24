from django.db import models
from subjects.models import Lesson


class Question(models.Model):
    """ questions table """
    body = models.TextField()
    difficulty = models.SmallIntegerField(
        choices=[
            (1, 'Easy'),
            (2, 'Medium'),
            (3, 'Hard'),
            (4, 'Very Hard')
        ]
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions')
    graph = models.ImageField(upload_to='graphs/', null=True, blank=True)

    def __str__(self):
        return self.body[:50]


class Answer(models.Model):
    """ answers table """
    body = models.CharField(max_length=256)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return self.body
