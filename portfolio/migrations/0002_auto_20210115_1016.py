# Generated by Django 2.2.5 on 2021-01-15 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0151_auto_20210105_1258'),
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userportfolio',
            name='chosenLearningObjs',
            field=models.ManyToManyField(blank=True, to='rubrics.LearningObjective'),
        ),
        migrations.AlterField(
            model_name='userportfolio',
            name='portfolio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.Portfolio'),
        ),
    ]
