# Generated by Django 4.0.2 on 2022-08-04 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Participate', '0004_clarification_is_answered'),
    ]

    operations = [
        migrations.AddField(
            model_name='clarification',
            name='answer',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]
