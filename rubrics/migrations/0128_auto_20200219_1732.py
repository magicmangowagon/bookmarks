# Generated by Django 2.2.5 on 2020-02-19 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0127_auto_20200219_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challengeresourcesfile',
            name='file',
            field=models.FileField(max_length=200, upload_to='resources/'),
        ),
    ]
