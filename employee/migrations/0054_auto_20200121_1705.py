# Generated by Django 2.2.7 on 2020-01-21 11:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0053_auto_20200121_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 21, 11, 20, 12, 859888, tzinfo=utc)),
        ),
    ]
