# Generated by Django 2.0.5 on 2018-11-06 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0011_auto_20181106_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learningobjective',
            name='loNumber',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8')]),
        ),
    ]
