""" this file contains the model for the paths table
"""

from core.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from grades.models.curriculum import Curriculum


class Path(BaseModel):
    """path model"""

    class MainLanguageChoices(models.TextChoices):
        """choices for the main language of the path"""

        ENGLISH = "ENGLISH", _("English")
        ARABIC = "ARABIC", _("Arabic")

    name = models.CharField(max_length=255)
    curriculum = models.ForeignKey(
        Curriculum,
        on_delete=models.CASCADE,
        related_name="paths",
        related_query_name="path",
    )
    main_language = models.CharField(
        max_length=32,
        choices=MainLanguageChoices.choices,
        default=MainLanguageChoices.ENGLISH,
    )

    class Meta:
        db_table = "paths"

    def __str__(self) -> str:
        return f"{self.curriculum} - {self.name}"
