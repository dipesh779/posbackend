# Generated by Django 2.2.7 on 2020-01-20 07:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0045_auto_20200120_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 20, 7, 45, 38, 297305, tzinfo=utc)),
        ),
    ]