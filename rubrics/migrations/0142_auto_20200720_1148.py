# Generated by Django 2.2.5 on 2020-07-20 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubrics', '0141_tfjeval_usersolution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tfjeval',
            name='question',
        ),
        migrations.AddField(
            model_name='tfjeval',
            name='question1',
            field=models.TextField(blank=True, default='', verbose_name='Why did you pick this TFJ learning objective?'),
        ),
        migrations.AddField(
            model_name='tfjeval',
            name='question2',
            field=models.TextField(blank=True, default='', verbose_name='How does TFJ intersect with this challenge and your solutions?'),
        ),
        migrations.AddField(
            model_name='tfjeval',
            name='question3',
            field=models.TextField(blank=True, default='', verbose_name='How do you interpret this learning objective?'),
        ),
        migrations.AddField(
            model_name='tfjeval',
            name='question4',
            field=models.TextField(blank=True, default='', verbose_name='What resources did you use to grow in this area?'),
        ),
        migrations.AddField(
            model_name='tfjeval',
            name='question5',
            field=models.TextField(blank=True, default='', verbose_name='How did this work move you forward in Teaching for Justice? What are your next steps for this competency?'),
        ),
    ]