""" This file is to define a model for the textbooks. """

import os

from core.models import BaseModel
from django.db import models
from PIL import Image


def cover_path(instance, filename: str) -> str:
    """returns the path of the cover image"""
    img_ext = os.path.splitext(filename)[1]
    return f"covers/{instance.__class__.__name__}/{instance.title}.{img_ext}"


class ResourceBase(BaseModel):
    """abstract base model for all the resources"""

    title = models.CharField(max_length=100)
    caption = models.TextField(
        blank=True,
        null=True,
        help_text="A brief description of the resource to add in the card.",
    )
    cover = models.ImageField(upload_to=cover_path, blank=True, null=True)
    syllabus_order = models.IntegerField(
        default=1,
        unique=True,
        help_text="The order of the resource in the syllabus.",
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        abstract = True
        ordering = ["syllabus_order"]

    def save(self, *args, **kwargs) -> None:
        """downsize the cover images before saving and updating"""
        super().save(*args, **kwargs)

        try:
            image = Image.open(self.cover.path)
            if image.height > 300 or image.width > 300:
                image.thumbnail((300, 300))
                image.save(self.cover.path)
        except FileNotFoundError:
            pass
