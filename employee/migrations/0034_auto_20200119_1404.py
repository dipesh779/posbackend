# Generated by Django 2.2.7 on 2020-01-19 08:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0033_auto_20200119_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 19, 8, 19, 27, 745943, tzinfo=utc)),
        ),
    ]