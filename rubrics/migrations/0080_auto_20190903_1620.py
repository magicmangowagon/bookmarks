# Generated by Django 2.1.7 on 2019-09-03 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0079_auto_20190903_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='solutions',
            field=models.ManyToManyField(blank=True, related_name='challenge_that_owns_me', to='rubrics.SolutionInstance'),
        ),
    ]