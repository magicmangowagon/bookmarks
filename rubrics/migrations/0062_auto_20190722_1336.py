# Generated by Django 2.1.7 on 2019-07-22 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0061_auto_20190712_1021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='degreeImplementation',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='scaleImplementation',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='typeImplementation',
        ),
    ]
