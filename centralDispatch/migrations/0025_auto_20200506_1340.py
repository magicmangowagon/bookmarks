# Generated by Django 2.2.5 on 2020-05-06 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0136_auto_20200302_1232'),
        ('centralDispatch', '0024_solutionstatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solutionstatus',
            name='challengeAccepted',
        ),
        migrations.CreateModel(
            name='ChallengeStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('challengeAccepted', models.BooleanField(default=False)),
                ('challenge', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='rubrics.Challenge')),
                ('solutionStatusByInstance', models.ManyToManyField(blank=True, default='', to='centralDispatch.SolutionStatus')),
            ],
        ),
    ]
