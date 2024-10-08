# Generated by Django 5.0.7 on 2024-10-09 18:34

import django.db.models.deletion
import questions.models.choice
import questions.models.questions
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("resources", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Question",
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
                    "difficulty",
                    models.CharField(
                        choices=[
                            ("easy", "Easy"),
                            ("medium", "Medium"),
                            ("hard", "Hard"),
                            ("very hard", "Very Hard"),
                        ],
                        default="easy",
                        max_length=32,
                    ),
                ),
                ("body", models.TextField()),
                (
                    "solution",
                    models.TextField(
                        blank=True,
                        help_text="Detailed solution (soluation manual)",
                        null=True,
                    ),
                ),
                (
                    "figure",
                    models.ImageField(
                        blank=True,
                        help_text="Question figure (diagram, graph, etc.)",
                        null=True,
                        upload_to=questions.models.questions.question_figure_path,
                    ),
                ),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        related_query_name="question",
                        to="resources.lesson",
                    ),
                ),
            ],
            options={
                "db_table": "questions",
                "ordering": ["?"],
            },
        ),
        migrations.CreateModel(
            name="Choice",
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
                ("body", models.TextField(blank=True, null=True)),
                (
                    "figure",
                    models.ImageField(
                        blank=True,
                        help_text="Choice figure (diagram, graph, etc.)",
                        null=True,
                        upload_to=questions.models.choice.choice_figure_path,
                    ),
                ),
                ("is_correct", models.BooleanField(default=False)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="choices",
                        related_query_name="choice",
                        to="questions.question",
                    ),
                ),
            ],
            options={
                "db_table": "choices",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Type",
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
                ("name", models.CharField(max_length=128)),
                (
                    "subject",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="types",
                        related_query_name="type",
                        to="resources.subject",
                    ),
                ),
            ],
            options={
                "db_table": "types",
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="question",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                related_query_name="question",
                to="questions.type",
            ),
        ),
        migrations.AddConstraint(
            model_name="choice",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("body__isnull", False), ("figure__isnull", False), _connector="OR"
                ),
                name="body_figure_not_null",
            ),
        ),
    ]
