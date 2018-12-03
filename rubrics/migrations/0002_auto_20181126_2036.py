# Generated by Django 2.1.2 on 2018-11-26 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersolution',
            name='challengeName',
        ),
        migrations.AddField(
            model_name='usersolution',
            name='challengeName',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rubrics.Challenge'),
        ),
    ]
