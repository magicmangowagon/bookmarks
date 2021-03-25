# Generated by Django 2.2.5 on 2020-08-21 16:21

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0146_auto_20200821_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='drivingQ',
            field=ckeditor_uploader.fields.RichTextUploadingField(default='', null=True, verbose_name='Driving Questions'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='soldThemes',
            field=ckeditor_uploader.fields.RichTextUploadingField(default='', null=True, verbose_name='SoLD Themes'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='tfjFocus',
            field=ckeditor_uploader.fields.RichTextUploadingField(default='', null=True, verbose_name='Teaching for Justice Focus'),
        ),
    ]