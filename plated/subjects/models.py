import os
from django.utils.text import slugify
from django.db import models
from curriculum.models import Grade, Semester
from PIL import Image

# Create your models here.

def resize_image(imgPath):
    """ resize image """
    try:
        image = Image.open(imgPath)
        if image.height > 300 or image.width > 300:
            image.thumbnail((400, 400))
            image.save(imgPath)
    except FileNotFoundError:
        pass


class Subject(models.Model):
    """ subjects table """
    name = models.CharField(max_length=128)
    cover = models.ImageField(default='default.jpg', upload_to='subject_covers')
    caption = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} subject"

    def save(self):
        """ changes the name of the cover and remove older one before saving """
        # changes the name of the cover image to be the_model_name-instance_pk.ext
        if self.cover:
            _, ext = os.path.splitext(self.cover.name)
            new_img_name = f"{slugify(self.__class__.__name__)}-{self.pk}{ext}"
            self.cover.name = new_img_name
        # If updating the cover image, remove the old one first, else do nothing
        if self.pk:
            try:
                old_cover = Subject.objects.get(pk=self.pk).cover
                if old_cover and old_cover.name != self.cover.name:
                    if os.path.isfile(old_cover.path):
                        os.remove(old_cover.path)
            except Subject.DoesNotExist:
                pass
        super().save()
        resize_image(self.cover.path)


class Unit(models.Model):
    """ units table """
    number = models.SmallIntegerField()
    title = models.CharField(max_length=128)
    subject = models.ForeignKey(Subject, related_name='units', on_delete=models.CASCADE)
    cover = models.ImageField(default='default.jpg', upload_to='unit_covers')
    caption = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Unit {self.number} : {self.title} - {self.subject.name}"

    def save(self, *args, **kwargs):
        """ changes the name of the cover and remove older one before saving """
        # changes the name of the cover image to be the_model_name-instance_pk.ext
        if self.cover:
            root, ext = os.path.splitext(self.cover.name)
            new_img_name = f"{slugify(self.__class__.__name__)}-{self.pk}{ext}"
            if not self.cover.name.endswith(new_img_name):
                self.cover.name = new_img_name
        # If updating the cover image, remove the old one first, else do nothing
        if self.pk:
            try:
                old_cover = Unit.objects.get(pk=self.pk).cover
                if old_cover and old_cover.name != self.cover.name:
                    if os.path.isfile(old_cover.path):
                        os.remove(old_cover.path)
            except Unit.DoesNotExist:
                pass
        super().save(*args, **kwargs)
        resize_image(self.cover.path)


class Chapter(models.Model):
    """ chapters table """
    number = models.SmallIntegerField()
    title = models.CharField(max_length=128)
    unit = models.ForeignKey(Unit, related_name='chapters', on_delete=models.CASCADE)
    cover = models.ImageField(default='default.jpg', upload_to='chapter_covers')
    caption = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Chapter {self.number} : {self.title} - {self.unit.title}"

    def save(self, *args, **kwargs):
        """ changes the name of the cover and remove older one before saving """
        # changes the name of the cover image to be the_model_name-instance_pk.ext
        if self.cover:
            root, ext = os.path.splitext(self.cover.name)
            new_img_name = f"{slugify(self.__class__.__name__)}-{self.pk}{ext}"
            if not self.cover.name.endswith(new_img_name):
                self.cover.name = new_img_name
        # If updating the cover image, remove the old one first, else do nothing
        if self.pk:
            try:
                old_cover = Unit.objects.get(pk=self.pk).cover
                if old_cover and old_cover.name != self.cover.name:
                    if os.path.isfile(old_cover.path):
                        os.remove(old_cover.path)
            except Unit.DoesNotExist:
                pass
        super().save(*args, **kwargs)
        resize_image(self.cover.path)


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
    grade = models.ForeignKey(Grade, related_name='lessons', on_delete=models.CASCADE, default=1)
    semester = models.ForeignKey(Semester, null=True, related_name='lessons', on_delete=models.CASCADE)

    def __str__(self):
        return f"Lesson {self.number} : {self.title} - {self.chapter.title}"

    def save(self, *args, **kwargs):
        """ changes the name of the cover and remove older one before saving """
        # changes the name of the cover image to be the_model_name-instance_pk.ext
        if self.cover:
            root, ext = os.path.splitext(self.cover.name)
            new_img_name = f"{slugify(self.__class__.__name__)}-{self.pk}{ext}"
            if not self.cover.name.endswith(new_img_name):
                self.cover.name = new_img_name
        # If updating the cover image, remove the old one first, else do nothing
        if self.pk:
            try:
                old_cover = Unit.objects.get(pk=self.pk).cover
                if old_cover and old_cover.name != self.cover.name:
                    if os.path.isfile(old_cover.path):
                        os.remove(old_cover.path)
            except Unit.DoesNotExist:
                pass
        super().save(*args, **kwargs)
        resize_image(self.cover.path)
