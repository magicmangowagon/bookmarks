# Generated by Django 2.0.5 on 2018-11-05 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0005_auto_20181105_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='learningobjective',
            name='competency',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='rubrics.Competency'),
            preserve_default=False,
        ),
    ]
