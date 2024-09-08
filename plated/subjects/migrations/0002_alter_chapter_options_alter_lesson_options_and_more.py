# Generated by Django 5.0.7 on 2024-09-08 11:18

import django.db.models.deletion
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0001_initial'),
        ('subjects', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'ordering': ['order_in_syllabus']},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['order_in_syllabus']},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='unit',
            options={'ordering': ['order_in_syllabus']},
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='grade',
        ),
        migrations.AddField(
            model_name='subject',
            name='grade',
            field=models.ForeignKey(default=uuid.UUID('24f0d529-1e65-4038-84e4-9600114d45ca'), on_delete=django.db.models.deletion.CASCADE, related_name='subjects', related_query_name='subject', to='curriculum.grade'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chapter',
            name='cover',
            field=models.ImageField(default='default.jpg', upload_to='covers/%(class)s/', verbose_name='cover image'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='number',
            field=models.SmallIntegerField(default=0, verbose_name='order in parent'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='order_in_syllabus',
            field=models.SmallIntegerField(default=1, verbose_name='order of in syllabus'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='cover',
            field=models.ImageField(default='default.jpg', upload_to='covers/%(class)s/', verbose_name='cover image'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='number',
            field=models.SmallIntegerField(default=0, verbose_name='order in parent'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='order_in_syllabus',
            field=models.SmallIntegerField(default=1, verbose_name='order of in syllabus'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='cover',
            field=models.ImageField(default='default.jpg', upload_to='covers/%(class)s/', verbose_name='cover image'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='cover',
            field=models.ImageField(default='default.jpg', upload_to='covers/%(class)s/', verbose_name='cover image'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='number',
            field=models.SmallIntegerField(default=0, verbose_name='order in parent'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='order_in_syllabus',
            field=models.SmallIntegerField(default=1, verbose_name='order of in syllabus'),
        ),
    ]
