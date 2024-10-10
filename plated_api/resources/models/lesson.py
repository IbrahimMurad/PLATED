""" This file is to define a model for the lessons of the units. """

import os

from django.core.exceptions import ValidationError
from django.db import models
from grades.models import Semester
from resources.models import Chapter, ResourceBase


def lesson_lecture_vid_path(instance, filename: str) -> str:
    """Returns the path for the lecture video"""
    file_ext = os.path.splitext(filename)[1]
    return f"videos/lessons/lectures/{instance.title}.{file_ext}"


def lesson_section_vid_path(instance, filename: str) -> str:
    """Returns the path for the section video"""
    file_ext = os.path.splitext(filename)[1]
    return f"videos/lessons/sections/{instance.title}.{file_ext}"


class Lesson(ResourceBase):
    """Lesson model for lessons table that holds lesson details."""

    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name="lessons",
        related_query_name="lesson",
    )
    semester = models.ForeignKey(
        Semester,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The semester this lesson belongs to in syllabus.",
    )
    intro = models.TextField(
        null=True,
        blank=True,
        help_text="A brief introduction of the lesson in a way to draw attention.",
    )
    goals = models.TextField(
        null=True, blank=True, help_text="What a student should gain after this lesson."
    )
    requires = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="required_by",
        help_text="This field holds the lessons"
        + " that should be completed before this lesson.",
    )
    details = models.TextField(
        null=True, blank=True, help_text="The main content of the lesson."
    )
    lecture_vid = models.FileField(
        null=True,
        blank=True,
        upload_to=lesson_lecture_vid_path,
        help_text="A video of the lecture for the lesson.",
    )
    section_vid = models.FileField(
        null=True,
        blank=True,
        upload_to=lesson_section_vid_path,
        help_text="A video for solving problems and answering questions of the lesson.",
    )

    class Meta:
        db_table = "lessons"
        ordering = ["chapter", "syllabus_order"]
        unique_together = ["chapter", "syllabus_order"]

    def add_lesson_to_requires(self, pre_lesson) -> None:
        """validate that the pre_lesson does not have
        this lesson (self) in its requires list,
        then add it if validated."""
        if self in pre_lesson.requires.all():
            raise ValidationError(
                f"{self.title} is already required by {pre_lesson.title}.\n"
                + "A lesson can not be required by and required for another lesson"
                + " at the same time."
            )
        self.requires.add(pre_lesson)
