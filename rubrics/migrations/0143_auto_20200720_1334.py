# Generated by Django 2.2.5 on 2020-07-20 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0142_auto_20200720_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='tfjeval',
            name='evaluator',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='rubrics.Evaluated'),
        ),
        migrations.AlterField(
            model_name='tfjeval',
            name='userSolution',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='rubrics.TfJSolution'),
        ),
    ]