from core.models import BaseModel
import os
from django.utils.text import slugify
from django.db import models
from curriculum.models import Grade, Semester
from .utils import resize_image


class MaterialBaseModel(BaseModel):
    """ an abstract base model for Subject, Unit, Chapter, and Lesson models """
    title = models.CharField(max_length=128)
    cover = models.ImageField(default='default.jpg', upload_to='covers')
    caption = models.TextField(null=True, blank=True)
    order_in_syllabus = models.SmallIntegerField(default=1)
    number = models.SmallIntegerField(default=1)

    def __str__(self):
        return f"{self.title} subject"

    def save(self, *args, **kwargs):
        """ changes the name of the cover and remove older one before saving """
        if self.cover:
            root, ext = os.path.splitext(self.cover.name)
            new_img_name = f"{slugify(self.__class__.__name__)}-{self.pk}{ext}"
            if not self.cover.name.endswith(new_img_name):
                self.cover.name = new_img_name
        # If updating the cover image, remove the old one first, else do nothing
        if self.pk:
            try:
                old_cover = self.__class__.objects.get(pk=self.pk).cover
                if old_cover and old_cover.name != self.cover.name:
                    if os.path.isfile(old_cover.path):
                        os.remove(old_cover.path)
            except self.__class__.DoesNotExist:
                pass
        super().save(*args, **kwargs)
        resize_image(self.cover.path)

    

    class Meta:
        abstract = True


class Subject(MaterialBaseModel):
    """ subjects table """
    order_in_syllabus = None
    number = None


class Unit(MaterialBaseModel):
    """ units table """
    subject = models.ForeignKey(Subject, related_name='units', on_delete=models.CASCADE)

class Chapter(MaterialBaseModel):
    """ chapters table """
    unit = models.ForeignKey(Unit, related_name='chapters', on_delete=models.CASCADE)


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
