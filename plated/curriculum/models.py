from django.db import models
from django.utils import timezone


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


class Semester(models.Model):
    """ semesters table """
    title = models.CharField(
        max_length=1,
        choices=[
            ("1", "first term"),
            ("2", "second term"),
            ("0", "No term"),
            ])
    starting_date = models.DateField()
    ending_date = models.DateField()

    def __str__(self):
        return f"{self.title}"


CURRENT_SEMESTER = Semester.objects.filter(
    starting_date__lte=timezone.now(),
    ending_date__gte=timezone.now()
    ).first()
