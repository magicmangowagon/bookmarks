# Generated by Django 2.1.7 on 2019-09-03 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0073_challenge_display'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='display',
            field=models.BooleanField(default=True, verbose_name='Show Challenge'),
        ),
    ]
