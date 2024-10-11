""" This module defines signals for the users app
"""

from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Student, Teacher, User


def get_group(name: str) -> Group:
    """Get a group by name"""
    return Group.objects.get(name=name)


@receiver(post_save, sender=Student)
def add_user_to_student_group(sender, instance, created, **kwargs):
    """Add user to student group when a new student is created"""
    if created:
        instance.user.groups.add(get_group("Student"))


@receiver(post_save, sender=Teacher)
def add_user_to_teacher_group(sender, instance, created, **kwargs):
    """Add user to teacher group when a new teacher is created"""
    if created:
        instance.user.groups.add(get_group("Teacher"))


@receiver(post_save, sender=User)
def add_user_to_admin_group(sender, instance, created, **kwargs):
    """Add user to admin group if the user's role is admin"""
    if created and instance.role == User.Role.ADMIN:
        instance.groups.add(get_group("Admin"))
