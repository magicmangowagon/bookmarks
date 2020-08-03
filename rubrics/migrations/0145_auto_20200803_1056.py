# Generated by Django 2.2.5 on 2020-08-03 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0144_auto_20200727_1443'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='learningobjective',
            options={'ordering': ['compGroup', 'compNumber', 'loNumber']},
        ),
        migrations.RemoveField(
            model_name='competency',
            name='learningObjs',
        ),
        migrations.AddField(
            model_name='competency',
            name='learningObjs',
            field=models.ManyToManyField(blank=True, to='rubrics.LearningObjective'),
        ),
    ]
