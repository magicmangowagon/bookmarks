# Generated by Django 2.2.5 on 2020-02-18 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0123_challengeresources_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challengeresources',
            name='name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
