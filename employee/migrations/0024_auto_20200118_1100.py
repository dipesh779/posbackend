# Generated by Django 2.2.7 on 2020-01-18 05:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0023_auto_20200117_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 18, 5, 15, 51, 509060, tzinfo=utc)),
        ),
    ]