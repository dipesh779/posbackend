# Generated by Django 2.2.7 on 2020-01-19 07:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0032_auto_20200119_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 19, 7, 46, 49, 143628, tzinfo=utc)),
        ),
    ]