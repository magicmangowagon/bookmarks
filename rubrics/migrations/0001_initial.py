# Generated by Django 2.1.2 on 2018-12-05 17:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djrichtextfield.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', djrichtextfield.models.RichTextField()),
            ],
        ),
        migrations.CreateModel(
            name='Competency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Criterion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='LearningObjective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compGroup', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F')], default='A', max_length=1)),
                ('compNumber', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')])),
                ('loNumber', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8')])),
                ('name', models.CharField(max_length=250)),
                ('evidenceMissing', models.TextField(blank=True)),
                ('evidencePresent', models.TextField(blank=True)),
                ('feedback', models.TextField(blank=True)),
                ('suggestions', models.TextField(blank=True)),
                ('readiness', models.BooleanField(blank=True)),
                ('completionLevel', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Rubric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=250)),
                ('completionLevel', models.IntegerField()),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rubrics.Challenge')),
                ('competencies', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rubrics.Competency')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RubricLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evidenceMissing', models.TextField()),
                ('evidencePresent', models.TextField()),
                ('feedback', models.TextField()),
                ('suggestions', models.TextField()),
                ('readiness', models.BooleanField()),
                ('learningObjective', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rubrics.LearningObjective')),
                ('rubric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rubrics.Rubric')),
            ],
        ),
        migrations.CreateModel(
            name='UserSolution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='uploads/')),
                ('solution', djrichtextfield.models.RichTextField()),
                ('challengeName', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rubrics.Challenge')),
                ('userOwner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='rubric',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rubrics.UserSolution'),
        ),
        migrations.AddField(
            model_name='criterion',
            name='learningObj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rubrics.LearningObjective'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='learningObjs',
            field=models.ManyToManyField(blank=True, to='rubrics.LearningObjective'),
        ),
    ]
