# Generated by Django 2.2.5 on 2020-01-30 21:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0119_challengeresourcesfile_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='challengeresourcesfile',
            options={'ordering': ['order']},
        ),
    ]