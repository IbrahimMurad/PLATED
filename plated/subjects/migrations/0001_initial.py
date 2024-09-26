# Generated by Django 5.0.7 on 2024-09-03 20:56

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("curriculum", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Chapter",
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
                ("title", models.CharField(max_length=128)),
                ("cover", models.ImageField(default="default.jpg", upload_to="covers")),
                ("caption", models.TextField(blank=True, null=True)),
                ("order_in_syllabus", models.SmallIntegerField(default=1)),
                ("number", models.SmallIntegerField(default=1)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Subject",
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
                ("title", models.CharField(max_length=128)),
                ("cover", models.ImageField(default="default.jpg", upload_to="covers")),
                ("caption", models.TextField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Lesson",
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
                ("title", models.CharField(max_length=128)),
                ("cover", models.ImageField(default="default.jpg", upload_to="covers")),
                ("caption", models.TextField(blank=True, null=True)),
                ("order_in_syllabus", models.SmallIntegerField(default=1)),
                ("number", models.SmallIntegerField(default=1)),
                ("intro", models.TextField(blank=True, null=True)),
                ("goals", models.TextField(blank=True, null=True)),
                ("details", models.TextField(blank=True, null=True)),
                (
                    "lecture_video",
                    models.FileField(blank=True, null=True, upload_to="lecture_videos"),
                ),
                (
                    "section_video",
                    models.FileField(
                        blank=True, null=True, upload_to="sections_videos"
                    ),
                ),
                ("starting_time", models.DateTimeField(blank=True, null=True)),
                ("ending_time", models.DateTimeField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                ("requires", models.JSONField(blank=True, null=True)),
                ("required_by", models.JSONField(blank=True, null=True)),
                (
                    "chapter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lessons",
                        to="subjects.chapter",
                    ),
                ),
                (
                    "grade",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lessons",
                        to="curriculum.grade",
                    ),
                ),
                (
                    "semester",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lessons",
                        to="curriculum.semester",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Unit",
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
                ("title", models.CharField(max_length=128)),
                ("cover", models.ImageField(default="default.jpg", upload_to="covers")),
                ("caption", models.TextField(blank=True, null=True)),
                ("order_in_syllabus", models.SmallIntegerField(default=1)),
                ("number", models.SmallIntegerField(default=1)),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="units",
                        to="subjects.subject",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="chapter",
            name="unit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="chapters",
                to="subjects.unit",
            ),
        ),
    ]
