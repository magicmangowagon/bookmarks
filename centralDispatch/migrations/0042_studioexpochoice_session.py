# Generated by Django 2.2.5 on 2020-08-27 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0009_auto_20200827_1526'),
        ('centralDispatch', '0041_studioexpochoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='studioexpochoice',
            name='session',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='info.BaseInfo'),
        ),
    ]