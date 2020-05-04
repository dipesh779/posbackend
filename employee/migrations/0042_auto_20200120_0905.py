# Generated by Django 2.2.7 on 2020-01-20 03:20

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_auto_20200120_0832'),
        ('employee', '0041_auto_20200120_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='database.CompanyDetail'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='dob',
            field=models.DateField(default=datetime.datetime(2020, 1, 20, 3, 20, 38, 438675, tzinfo=utc)),
        ),
    ]