# Generated by Django 2.2.7 on 2020-01-20 07:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0046_auto_20200120_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 20, 7, 49, 27, 7968, tzinfo=utc)),
        ),
    ]