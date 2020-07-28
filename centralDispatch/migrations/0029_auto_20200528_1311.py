# Generated by Django 2.2.5 on 2020-05-28 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('centralDispatch', '0028_auto_20200528_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentkeeper',
            name='coach',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(('role', 2), ('role', 3), ('role', 4), _connector='OR'), null=True, on_delete=django.db.models.deletion.PROTECT, related_name='coach', to='account.Profile'),
        ),
    ]