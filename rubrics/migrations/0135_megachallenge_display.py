# Generated by Django 2.2.5 on 2020-02-27 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0134_auto_20200227_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='megachallenge',
            name='display',
            field=models.BooleanField(default=True, verbose_name='Show Challenge'),
        ),
    ]
