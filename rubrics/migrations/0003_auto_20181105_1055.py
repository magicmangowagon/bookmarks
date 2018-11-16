# Generated by Django 2.0.5 on 2018-11-05 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0002_auto_20181102_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rubric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name='learningobjective',
            name='completionLevel',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='learningobjective',
            name='evidenceMissing',
            field=models.TextField(default='default'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='learningobjective',
            name='evidencePresent',
            field=models.TextField(default='default'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='learningobjective',
            name='feedback',
            field=models.TextField(default='default'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rubric',
            name='learningObjs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rubrics.LearningObjective'),
        ),
    ]
