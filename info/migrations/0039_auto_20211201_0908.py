# Generated by Django 2.2.4 on 2021-12-01 14:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0038_auto_20211201_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseinfo',
            name='occurrenceDate',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 1, 9, 8, 3, 182470)),
        ),
        migrations.AlterField(
            model_name='commentcontainer',
            name='highlight',
            field=models.CharField(blank=True, default='', max_length=2000),
        ),
    ]
