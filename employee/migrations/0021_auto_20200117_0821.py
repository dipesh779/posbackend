# Generated by Django 2.2.7 on 2020-01-17 08:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0020_auto_20200117_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 17, 8, 21, 41, 551992, tzinfo=utc)),
        ),
    ]
