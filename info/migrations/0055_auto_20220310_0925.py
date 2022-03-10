# Generated by Django 2.2.4 on 2022-03-10 14:25

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('info', '0054_auto_20220308_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseinfo',
            name='occurrenceDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 10, 9, 25, 9, 806974)),
        ),
        migrations.CreateModel(
            name='ContentFlag',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='info.BaseModel')),
                ('like', models.BooleanField(default=False)),
                ('favorite', models.BooleanField(default=False)),
                ('add', models.BooleanField(default=False)),
                ('content', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='info.LearningModulePageSection')),
                ('share', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('info.basemodel',),
        ),
    ]
