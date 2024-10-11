""" This module defines a custom user model for this project
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model for this project"""

    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        STUDENT = "STUDENT", _("Student")
        TEACHER = "TEACHER", _("Teacher")

    email = models.EmailField(_("Email"), unique=True)
    username = models.CharField(_("UserName"), max_length=150, unique=False)
    phone_number = models.CharField(
        _("Phone Number"), max_length=15, blank=True, null=True
    )
    birth_date = models.DateField(_("Date of Birth"), blank=True, null=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.ADMIN)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "auth_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def is_student(self):
        return self.role == self.Role.STUDENT

    def is_teacher(self):
        return self.role == self.Role.TEACHER

    def is_admin(self):
        return self.role == self.Role.ADMIN
