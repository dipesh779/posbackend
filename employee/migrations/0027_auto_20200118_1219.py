# Generated by Django 2.2.7 on 2020-01-18 06:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0026_auto_20200118_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 18, 6, 34, 38, 748601, tzinfo=utc)),
        ),
    ]