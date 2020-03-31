# Generated by Django 2.2.5 on 2020-03-31 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('centralDispatch', '0011_auto_20200331_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentkeeper',
            name='coach',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='coach', to='account.Profile'),
        ),
        migrations.AlterField(
            model_name='assignmentkeeper',
            name='evaluator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='evaluator', to='account.Profile'),
        ),
    ]
