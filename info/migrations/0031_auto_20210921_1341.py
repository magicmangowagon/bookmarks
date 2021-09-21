# Generated by Django 2.2.5 on 2021-09-21 17:41

import datetime
from django.db import migrations, models
import djrichtextfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0030_auto_20210920_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prompts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, default='', max_length=500)),
                ('response', djrichtextfield.models.RichTextField()),
            ],
        ),
        migrations.AlterField(
            model_name='baseinfo',
            name='occurrenceDate',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 21, 13, 41, 48, 475689)),
        ),
        migrations.AddField(
            model_name='baseinfo',
            name='prompts',
            field=models.ManyToManyField(blank=True, to='info.Prompts'),
        ),
    ]
