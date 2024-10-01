""" this file contains the model for the curriculums table
"""

from core.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Curriculum(BaseModel):
    """curriculum model"""

    class CurriculumType(models.TextChoices):
        """choices for the type of curriculum"""

        NATIONAL = "NATIONAL", _("National")
        INTERNATIONAL = "INTERNATIONAL", _("International")

    name = models.CharField(
        max_length=255, unique=True
    )  # uniqueness is for conflict resolution
    type = models.CharField(
        max_length=32, choices=CurriculumType.choices, default=CurriculumType.NATIONAL
    )

    class Meta:
        db_table = "curriculums"

    def __str__(self) -> str:
        return self.name
