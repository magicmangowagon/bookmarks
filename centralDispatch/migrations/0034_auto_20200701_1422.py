# Generated by Django 2.2.5 on 2020-07-01 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centralDispatch', '0033_auto_20200617_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challengestatus',
            name='solutionStatusByInstance',
            field=models.ManyToManyField(blank=True, default='', related_name='challengestatus', to='centralDispatch.SolutionStatus'),
        ),
    ]