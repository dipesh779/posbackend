# Generated by Django 2.2.7 on 2020-01-16 03:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_auto_20200115_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 16, 3, 40, 33, 583959, tzinfo=utc)),
        ),
    ]
