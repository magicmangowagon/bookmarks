# Generated by Django 2.2.5 on 2021-01-19 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0151_auto_20210105_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='megachallenge',
            name='collapse',
            field=models.BooleanField(default=False, verbose_name='Collapse sub challenges'),
        ),
    ]