# Generated by Django 2.1.7 on 2019-03-19 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0018_auto_20190315_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='rubricline',
            name='needsLaterAttention',
            field=models.CharField(choices=[('A', 'Yes'), ('B', 'No')], default='', max_length=1),
        ),
        migrations.AddField(
            model_name='rubricline',
            name='ready',
            field=models.BooleanField(default=False),
        ),
    ]
