# Generated by Django 3.1.2 on 2020-10-28 16:24

from django.db import migrations
import pyuploadcare.dj.models


class Migration(migrations.Migration):

    dependencies = [
        ('awwards', '0015_auto_20201028_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='img',
            field=pyuploadcare.dj.models.ImageField(blank=True),
        ),
    ]
