# Generated by Django 2.1.7 on 2019-07-22 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0062_auto_20190722_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='CLASSROOMEVIDENCE',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='challenge',
            name='DESIGN',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='challenge',
            name='FULLCLASS',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='challenge',
            name='IMPLEMENT',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='challenge',
            name='OBSERVATION',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='challenge',
            name='ONEONONE',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='challenge',
            name='REFLECTION',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='challenge',
            name='SIMULATE',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='challenge',
            name='SMALLGROUP',
            field=models.BooleanField(default=False),
        ),
    ]
