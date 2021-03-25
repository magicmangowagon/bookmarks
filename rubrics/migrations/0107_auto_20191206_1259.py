# Generated by Django 2.2.5 on 2019-12-06 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0106_auto_20191202_1320'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='challenge',
            options={'ordering': ['my_order']},
        ),
        migrations.AlterModelOptions(
            name='megachallenge',
            options={'ordering': ['my_order']},
        ),
        migrations.AddField(
            model_name='challenge',
            name='my_order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='megachallenge',
            name='my_order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]