# Generated by Django 2.2.7 on 2020-01-16 08:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0011_auto_20200116_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 16, 8, 59, 47, 835565, tzinfo=utc)),
        ),
    ]
