from django.db import models
from users.models import Student
from subjects.models import Subject, Unit, Chapter, Lesson
from questions.models import Question, Answer
from datetime import timedelta


class Exam(models.Model):
    """ exams table """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    solved_at = models.DateTimeField(null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exams')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True, related_name='exams')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, related_name='exams')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True, related_name='exams')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True, related_name='exams')
    duration = models.DurationField(default=timedelta(hours=1), null=True, blank=True)
    questions = models.ManyToManyField(Question)
    score = models.IntegerField(null=True, blank=True)

    @property
    def max_score(self):
        """ returns the maximum score of the exam """
        return self.questions.count()
    
    @property
    def score_percentage(self):
        """ returns the score as a percentage for the exam """
        if self.max_score == 0:
            return 0
        return (self.score / self.max_score) * 100

    def __str__(self):
        return f"Exam on {self.subject or self.unit or self.chapter or self.lesson} by {self.student}"


class StudentAnswer(models.Model):
    """ student_answers table """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    
    class Meta:
        """ adds a unique combination of student, exam, and answer constraint """
        unique_together = ('student', 'exam', 'answer')

    def __str__(self):
        return f"{self.exam.student} answered {self.answer} in {self.exam}"
