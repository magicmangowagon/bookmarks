# Generated by Django 2.2.5 on 2021-09-17 17:09

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0023_auto_20210917_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseinfo',
            name='occurrenceDate',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 17, 13, 9, 12, 703727)),
        ),
        migrations.CreateModel(
            name='CommentContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='info.QuestionStub')),
            ],
        ),
    ]
