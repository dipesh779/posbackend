# Generated by Django 2.2.7 on 2020-01-15 16:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_auto_20200115_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 15, 16, 16, 45, 859709, tzinfo=utc)),
        ),
    ]