# Generated by Django 2.1.2 on 2019-01-11 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0002_auto_20190108_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
