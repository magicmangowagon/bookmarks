# Generated by Django 2.1.7 on 2019-05-23 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0034_auto_20190522_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersolution',
            name='solution',
            field=models.CharField(max_length=2000),
        ),
    ]
