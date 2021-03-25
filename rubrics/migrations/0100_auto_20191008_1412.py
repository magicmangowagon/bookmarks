# Generated by Django 2.2.5 on 2019-10-08 18:12

from django.db import migrations, models
import django.db.models.deletion
import djrichtextfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0099_coachreview_evaluator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criterion',
            name='learningObj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learningObj_that_owns_me', to='rubrics.LearningObjective'),
        ),
        migrations.AlterField(
            model_name='usersolution',
            name='solution',
            field=djrichtextfield.models.RichTextField(),
        ),
    ]