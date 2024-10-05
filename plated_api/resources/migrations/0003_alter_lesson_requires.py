# Generated by Django 5.0.7 on 2024-10-05 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resources", "0002_alter_lesson_requires"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="requires",
            field=models.ManyToManyField(
                blank=True,
                help_text="This field holds the lessons that should be completed before this lesson.",
                related_name="required_by",
                to="resources.lesson",
            ),
        ),
    ]
