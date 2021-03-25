# Generated by Django 2.1.7 on 2019-05-28 19:15

from django.db import migrations, models
import django.db.models.deletion
import djrichtextfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0036_auto_20190523_1205'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearningExperience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=600)),
                ('description', djrichtextfield.models.RichTextField()),
                ('challenge', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='challenge', to='rubrics.Challenge')),
            ],
        ),
    ]