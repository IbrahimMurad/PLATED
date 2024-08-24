from django.db import models
from django.contrib.auth.models import User
from curriculum.models import Grade
from subjects.models import Lesson


class Student(models.Model):
    """ students table """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    tagged_lessons = models.ManyToManyField(Lesson, related_name='tagged_students')

    def __str__(self):
        return f"Student: {self.first_name} {self.last_name}"
