# Generated by Django 3.2.13 on 2022-05-14 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson_8', '0002_gamerlibrarymodel_gamermodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamermodel',
            name='nickname',
            field=models.CharField(max_length=64),
        ),
    ]
