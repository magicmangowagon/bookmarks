# Generated by Django 2.1.2 on 2018-12-04 17:50

from django.db import migrations
import djrichtextfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0005_auto_20181204_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersolution',
            name='solution',
            field=djrichtextfield.models.RichTextField(default=''),
            preserve_default=False,
        ),
    ]
