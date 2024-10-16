# Generated by Django 5.0.7 on 2024-10-13 12:33

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("grades", "0005_alter_semester_curriculum"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Class",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(
                        max_length=128, verbose_name="The name of the class"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="The description of the class",
                    ),
                ),
                (
                    "grade",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="classes",
                        related_query_name="class",
                        to="grades.grade",
                    ),
                ),
                (
                    "students",
                    models.ManyToManyField(
                        related_name="classes",
                        related_query_name="class",
                        to="users.student",
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="classes",
                        related_query_name="class",
                        to="users.teacher",
                    ),
                ),
            ],
            options={
                "verbose_name": "Class",
                "verbose_name_plural": "Classes",
                "db_table": "classes",
            },
        ),
    ]
