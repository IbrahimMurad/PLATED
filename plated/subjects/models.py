from django.db import models
from curriculum.models import Grade

# Create your models here.

class Subject(models.Model):
    """ subjects table """
    name = models.CharField(max_length=128)
    grade = models.ForeignKey(Grade, models.SET_NULL, null=True, blank=True)
    cover_pic = models.ImageField(default='default.jpg', upload_to='subject_covers')
    caption = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} for {self.grade}"


class Unit(models.Model):
    """ units table """
    number = models.SmallIntegerField()
    title = models.CharField(max_length=128)
    subject = models.ForeignKey(Subject, related_name='units', on_delete=models.CASCADE)
    cover = models.ImageField(default='default.jpg', upload_to='unit_covers')
    caption = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Unit {self.number} : {self.title} - {self.subject.name}"


class Chapter(models.Model):
    """ chapters table """
    number = models.SmallIntegerField()
    title = models.CharField(max_length=128)
    unit = models.ForeignKey(Unit, related_name='chapters', on_delete=models.CASCADE)
    cover = models.ImageField(default='default.jpg', upload_to='chapter_covers')
    caption = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Chapter {self.number} : {self.title} - {self.unit.title}"


class Lesson(models.Model):
    """ lessons table """
    updated_at = models.DateTimeField(auto_now=True)
    chapter = models.ForeignKey(Chapter, related_name='lessons', on_delete=models.CASCADE)
    number = models.SmallIntegerField()
    title = models.CharField(max_length=128)
    caption = models.TextField(null=True, blank=True)
    intro = models.TextField(null=True, blank=True)
    goals = models.TextField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    lecture_video = models.FileField(upload_to='lecture_videos', null=True, blank=True)
    section_video = models.FileField(upload_to='sections_videos', null=True, blank=True)
    starting_time = models.DateTimeField(null=True, blank=True)
    ending_time = models.DateTimeField(null=True, blank=True)
    cover = models.ImageField(default='default.jpg', upload_to='lesson_covers')
    notes = models.TextField(null=True, blank=True)
    requires = models.JSONField(null=True, blank=True)
    required_by = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Lesson {self.number} : {self.title} - {self.chapter.title}"
