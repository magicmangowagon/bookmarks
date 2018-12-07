# Generated by Django 2.1.2 on 2018-12-05 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0002_auto_20181205_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='competency',
            name='compGroup',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F')], default='A', max_length=1),
        ),
        migrations.AddField(
            model_name='competency',
            name='compNumber',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], default=1),
            preserve_default=False,
        ),
    ]