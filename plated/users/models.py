from core.models import BaseModel
from django.db import models
from django.contrib.auth.models import User
from curriculum.models import Grade
from subjects.models import Lesson


class Student(BaseModel):
    """ students table """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    tagged_lessons = models.ManyToManyField(Lesson, related_name='tagging_students', blank=True)

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    def __str__(self):
        return f"Student: {self.first_name} {self.last_name}"
