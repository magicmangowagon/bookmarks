# Generated by Django 2.1.2 on 2018-12-12 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0002_rubricline_rubric'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rubricline',
            name='rubric',
        ),
    ]