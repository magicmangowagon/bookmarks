# Generated by Django 2.1.2 on 2019-01-29 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0009_auto_20190129_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='criterialine',
            name='student',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='rubrics.UserSolution'),
            preserve_default=False,
        ),
    ]
