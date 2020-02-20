# Generated by Django 2.1.7 on 2019-04-10 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0023_competencyprogress'),
    ]

    operations = [
        migrations.AddField(
            model_name='competencyprogress',
            name='attempted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='competencyprogress',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
