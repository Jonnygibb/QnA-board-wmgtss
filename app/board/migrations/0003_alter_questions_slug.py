# Generated by Django 4.0.1 on 2022-01-26 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
