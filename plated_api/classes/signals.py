from classes.models import Class
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


@receiver(m2m_changed, sender=Class.students.through)
def validate_and_update_teacher_max_students(
    sender, instance, action, reverse, model, pk_set, **kwargs
) -> None:
    """Validate teacher's max_students based on
    the number of students intended to add"""
    teacher = instance.teacher

    if action == "pre_add":
        students_to_add: int = len(pk_set) if pk_set else 0
        if students_to_add > teacher.available_students:
            raise ValidationError(
                message=(
                    f"Cannot add {students_to_add} students."
                    f"Teacher can only accept {teacher.available_students}"
                    " more students."
                )
            )
