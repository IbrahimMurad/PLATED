""" Unit model
"""

from django.db import models
from django.urls import reverse
from subjects.models.base import MaterialBaseModel
from .chapters import Chapter
from curriculum.models import Semester
from curriculum.context_processors import CURRENT_SEMESTER


class RelevantLessonManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(semester=CURRENT_SEMESTER)


class Lesson(MaterialBaseModel):
    """lessons table"""

    # related to the chapter
    chapter = models.ForeignKey(
        Chapter,
        related_name="lessons",
        related_query_name="lesson",
        on_delete=models.CASCADE,
    )

    # lesson details
    intro = models.TextField(null=True, blank=True)
    goals = models.TextField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)

    # lesson resources
    lecture_video = models.FileField(upload_to="lecture_videos", null=True, blank=True)
    section_video = models.FileField(upload_to="sections_videos", null=True, blank=True)

    # lesson's best time for study
    starting_time = models.DateTimeField(null=True, blank=True)
    ending_time = models.DateTimeField(null=True, blank=True)

    # extra notes
    notes = models.TextField(null=True, blank=True)

    # prerequisites and requirements
    requires = models.JSONField(null=True, blank=True)
    required_by = models.JSONField(null=True, blank=True)

    # relevant to
    semester = models.ForeignKey(
        Semester,
        null=True,
        blank=True,
        related_name="lessons",
        related_query_name="lesson",
        on_delete=models.CASCADE,
    )

    objects = models.Manager()
    relevant = RelevantLessonManager()

    def get_absolute_url(self):
        return reverse("lesson-details", kwargs={"pk": self.pk})
