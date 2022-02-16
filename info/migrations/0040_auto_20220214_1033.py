# Generated by Django 2.2.4 on 2022-02-14 15:33

import ckeditor_uploader.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('info', '0039_auto_20211201_0908'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateCreated', models.DateTimeField(auto_created=True)),
                ('creator', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='baseinfo',
            name='occurrenceDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 14, 10, 33, 27, 682854)),
        ),
        migrations.CreateModel(
            name='LearningModulePrompt',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='info.BaseModel')),
                ('promptText', ckeditor_uploader.fields.RichTextUploadingField(default='')),
            ],
            bases=('info.basemodel',),
        ),
        migrations.CreateModel(
            name='LearningModuleResponse',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='info.BaseModel')),
                ('question', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='info.LearningModulePrompt')),
            ],
            bases=('info.basemodel',),
        ),
        migrations.CreateModel(
            name='LearningModulePage',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='info.BaseModel')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(default='')),
                ('pageNumber', models.IntegerField(default=0)),
                ('prompt', models.ManyToManyField(blank=True, to='info.LearningModulePrompt')),
            ],
            bases=('info.basemodel',),
        ),
        migrations.CreateModel(
            name='LearningModule',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='info.BaseModel')),
                ('name', models.CharField(default='', max_length=1000)),
                ('pages', models.ManyToManyField(blank=True, to='info.LearningModulePage')),
            ],
            bases=('info.basemodel',),
        ),
    ]
