# Generated by Django 2.2.7 on 2020-01-16 07:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0007_auto_20200116_0340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 16, 7, 45, 50, 222834, tzinfo=utc)),
        ),
    ]
