# Generated by Django 2.2.5 on 2020-08-19 19:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0005_auto_20200819_1418'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baseinfo',
            name='category',
        ),
        migrations.AddField(
            model_name='baseinfo',
            name='category',
            field=models.ManyToManyField(blank=True, to='info.InfoCategory'),
        ),
        migrations.AlterField(
            model_name='baseinfo',
            name='occurrenceDate',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 19, 15, 5, 12, 444701)),
        ),
    ]
