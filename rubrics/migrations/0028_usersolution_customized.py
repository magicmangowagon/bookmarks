# Generated by Django 2.1.7 on 2019-04-30 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0027_auto_20190429_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersolution',
            name='customized',
            field=models.BooleanField(default=False),
        ),
    ]
