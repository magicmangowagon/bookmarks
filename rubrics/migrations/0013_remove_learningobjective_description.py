# Generated by Django 2.0.5 on 2018-11-06 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0012_auto_20181106_1119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='learningobjective',
            name='description',
        ),
    ]
