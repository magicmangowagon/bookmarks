# Generated by Django 2.2.4 on 2022-02-21 16:26

import ckeditor_uploader.fields
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0154_temptfjsolution'),
        ('info', '0048_auto_20220221_1111'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewLearningObjective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='')),
                ('criteria', models.ManyToManyField(blank=True, default='', to='rubrics.Criterion')),
            ],
        ),
        migrations.AddField(
            model_name='learningmodulepagesection',
            name='name',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='baseinfo',
            name='occurrenceDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 21, 11, 26, 33, 292600)),
        ),
        migrations.AlterField(
            model_name='learningmodulepagesection',
            name='learningObjectives',
            field=models.ManyToManyField(blank=True, default='', to='info.NewLearningObjective'),
        ),
        migrations.AlterField(
            model_name='learningmoduleprompt',
            name='promptText',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=''),
        ),
    ]
