from classes.models import Class
from core.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from questions.models import Question
from resources.models import Chapter, Lesson, TextBook, Unit
from users.models import User


class Exam(BaseModel):

    class ScopeType(models.TextChoices):
        LESSON: tuple = "Lesson", _("Lesson")
        CHAPTER: tuple = "Chapter", _("Chapter")
        UNIT: tuple = "Unit", _("Unit")
        TEXTBOOK: tuple = "TextBook", _("Textbook")
        MULTIPLE: tuple = "Multiple", _("Multiple")

    title = models.CharField(
        "An optional title for the exam", max_length=255, null=True, blank=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="exams",
        related_query_name="exam",
    )
    classes = models.ManyToManyField(
        Class, related_name="exams", related_query_name="exam", blank=True
    )
    start_date = models.DateTimeField()
    duration = models.IntegerField()
    scope_type = models.CharField(
        max_length=10,
        choices=ScopeType.choices,
        default=ScopeType.LESSON,
    )
    scope_id = models.UUIDField(
        null=True,
        blank=True,
        help_text="The id of the scope object (Lesson, Chapter, Unit, or TextBook).",
    )
    multi_scope = models.ManyToManyField(Lesson, blank=True)
    questions = models.ManyToManyField(Question, through="ExamQuestions")

    class Meta:
        verbose_name = "Exam"
        verbose_name_plural = "Exams"
        indexes = [
            models.Index(fields=["scope_type", "scope_id"]),
        ]

    def save(self, *args, **kwargs) -> None:
        if self.scope_type == self.ScopeType.MULTIPLE:
            self.scope_id = None
        else:
            self.multi_scope.clear()

        if self.created_by.is_student:
            self.classes.clear()

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title | f"Exam by {self.created_by}"

    def get_scope(self) -> object:
        """Get the scope object of the exam if not multiple."""
        if self.scope_type == self.ScopeType.LESSON:
            return Lesson.objects.get(id=self.scope_id)
        elif self.scope_type == self.ScopeType.CHAPTER:
            return Chapter.objects.get(id=self.scope_id)
        elif self.scope_type == self.ScopeType.UNIT:
            return Unit.objects.get(id=self.scope_id)
        elif self.scope_type == self.ScopeType.TEXTBOOK:
            return TextBook.objects.get(id=self.scope_id)
        else:
            return None
