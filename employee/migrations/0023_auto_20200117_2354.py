# Generated by Django 2.2.7 on 2020-01-17 18:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0022_auto_20200117_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 17, 18, 9, 48, 785233, tzinfo=utc)),
        ),
    ]
