# Generated by Django 2.2.5 on 2020-08-28 19:21

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djrichtextfield.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rubrics', '0149_auto_20200821_1225'),
        ('info', '0009_auto_20200827_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseinfo',
            name='occurrenceDate',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 28, 15, 21, 26, 344936)),
        ),
        migrations.CreateModel(
            name='DiscussionTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDate', models.DateTimeField(auto_created=True)),
                ('title', models.CharField(default='', max_length=500)),
                ('creator', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DiscussionBoard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', djrichtextfield.models.RichTextField()),
                ('challenge', models.ManyToManyField(blank=True, default='', to='rubrics.Challenge')),
                ('topic', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='info.DiscussionTopic')),
            ],
        ),
    ]
