from django.db import models
from users.models import Student
from subjects.models import Subject, Unit, Chapter, Lesson
from questions.models import Question, Answer
from datetime import timedelta


class Exam(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    solved_at = models.DateTimeField(null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    duration = models.DurationField(default=timedelta(hours=1), null=True, blank=True)
    questions = models.ManyToManyField(Question)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"Exam on {self.subject or self.unit or self.chapter or self.lesson} by {self.student}"


class StudentAnswer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('student', 'exam', 'answer')

    def __str__(self):
        return f"{self.exam.student} answered {self.answer} in {self.exam}"
