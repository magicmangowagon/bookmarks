# Generated by Django 2.2.5 on 2020-07-10 17:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('centralDispatch', '0036_auto_20200710_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solutionstatus',
            name='returnTo',
            field=models.ForeignKey(default='', limit_choices_to=models.Q(U='s'), null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
