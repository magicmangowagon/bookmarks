# Generated by Django 2.1.7 on 2019-07-30 15:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rubrics', '0067_auto_20190724_1634'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('whoEvaluated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='usersolution',
            name='evaluated',
            field=models.ManyToManyField(blank=True, to='rubrics.Evaluated'),
        ),
    ]
