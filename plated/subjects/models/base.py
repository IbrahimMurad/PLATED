""" A module for defining the base model for all the models of subjects app,
in which, save method is edited to remove old cover pic and rename pased on the id of the instance
it also resizes the cover to save memory and reduce the sending time to client.
"""

from core.models import BaseModel
import os
from django.db import models
from subjects.utils import resize_image, get_upload_path


class MaterialBaseModel(BaseModel):
    """ an abstract base model for Subject, Unit, Chapter, and Lesson models """
    title = models.CharField(max_length=128)

    cover = models.ImageField(
        "cover image",
        default='default.jpg',
        upload_to=get_upload_path   # file name : id.jpg (changes before saving in save method)
    )

    # a caption for the card dispaly
    caption = models.TextField(null=True, blank=True)

    order_in_syllabus = models.SmallIntegerField(
        "order of in syllabus",
        default=1
    )

    # its default is 0 indicating that this this the only one (the only lesson in the chapter)
    number = models.SmallIntegerField(
        "order in parent",
        default=0,
    )

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        """ changes the name of the cover and remove older one before saving """
        if self.cover:
            root, ext = os.path.splitext(self.cover.name)
            new_img_name = f"{self.pk}{ext}"
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

        # resize after saving
        resize_image(self.cover.path)

    class Meta:
        abstract = True
        ordering = ['order_in_syllabus']
