""" Unit model
"""

from django.db import models
from subjects.models.base import MaterialBaseModel
from .chapters import Chapter
from curriculum.models import Grade, Semester


class Lesson(MaterialBaseModel):
    """ lessons table """
    
    # related to the chapter
    chapter = models.ForeignKey(Chapter, related_name='lessons', on_delete=models.CASCADE)

    # lesson details
    intro = models.TextField(null=True, blank=True)
    goals = models.TextField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)

    # lesson resources
    lecture_video = models.FileField(upload_to='lecture_videos', null=True, blank=True)
    section_video = models.FileField(upload_to='sections_videos', null=True, blank=True)

    # lesson's best time for study
    starting_time = models.DateTimeField(null=True, blank=True)
    ending_time = models.DateTimeField(null=True, blank=True)

    # extra notes
    notes = models.TextField(null=True, blank=True)

    # prerequisites and requirements
    requires = models.JSONField(null=True, blank=True)
    required_by = models.JSONField(null=True, blank=True)

    # relevant to
    grade = models.ForeignKey(Grade, related_name='lessons', on_delete=models.CASCADE, default=1)
    semester = models.ForeignKey(Semester, null=True, related_name='lessons', on_delete=models.CASCADE)
