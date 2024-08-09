from django.db import models
from django.utils import timezone

# Create your models here.

class Curriculum(models.Model):
    """ curriculums table """
    name = models.CharField(max_length=32, default="arabic")

    def __str__(self):
        return f"{self.name} curriculum"

class Grade(models.Model):
    """ grades table """
    title = models.CharField(max_length=64)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.curriculum}"
