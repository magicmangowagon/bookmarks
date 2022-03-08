# Generated by Django 2.2.4 on 2022-03-08 17:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0053_auto_20220302_1122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='learningmodulepagesection',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='learningmodulepagesection',
            name='title',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='baseinfo',
            name='occurrenceDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 8, 12, 0, 29, 129334)),
        ),
    ]
