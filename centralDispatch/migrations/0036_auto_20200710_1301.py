# Generated by Django 2.2.5 on 2020-07-10 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('centralDispatch', '0035_auto_20200710_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solutionstatus',
            name='returnTo',
            field=models.ForeignKey(default='', limit_choices_to={'User__profile__role__gte: 2'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
