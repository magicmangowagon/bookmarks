# Generated by Django 2.2.5 on 2020-07-01 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0137_auto_20200611_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersolution',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]