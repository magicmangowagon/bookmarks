# Generated by Django 2.2.5 on 2020-08-27 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0149_auto_20200821_1225'),
        ('centralDispatch', '0043_auto_20200827_1536'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studioexpochoice',
            name='learningExpoChoice',
        ),
        migrations.AddField(
            model_name='studioexpochoice',
            name='learningExpoChoice',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='rubrics.LearningExperience'),
        ),
    ]
