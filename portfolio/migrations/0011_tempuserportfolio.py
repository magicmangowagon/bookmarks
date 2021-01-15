# Generated by Django 2.2.5 on 2021-01-15 19:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0151_auto_20210105_1258'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portfolio', '0010_userportfolio_finalrubric'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempUserPortfolio',
            fields=[
                ('usersolution_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='rubrics.UserSolution')),
                ('team', models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('rubrics.usersolution',),
        ),
    ]
