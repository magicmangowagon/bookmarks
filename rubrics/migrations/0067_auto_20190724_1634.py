# Generated by Django 2.1.7 on 2019-07-24 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0066_auto_20190724_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criterialine',
            name='achievement',
            field=models.CharField(choices=[('0', '--'), ('A', 'Yes'), ('B', 'No'), ('C', 'Evidence for and against')], default='', max_length=1),
        ),
    ]
