# Generated by Django 3.1.2 on 2020-10-27 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awwards', '0002_auto_20201026_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='img',
            field=models.ImageField(default='default.png', upload_to='images'),
        ),
    ]
