# Generated by Django 2.2.7 on 2020-01-20 02:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0040_auto_20200120_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 20, 2, 48, 27, 960557, tzinfo=utc)),
        ),
    ]
