# Generated by Django 2.1.2 on 2019-01-29 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0006_rubricline_criteria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rubricline',
            name='criteria',
        ),
    ]
