# Generated by Django 2.2.7 on 2020-01-22 13:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0059_auto_20200122_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='purchase_order_date',
            field=models.DateField(default=datetime.datetime(2020, 1, 22, 13, 22, 18, 582802, tzinfo=utc), verbose_name='purchase order date'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='shipping_date',
            field=models.DateField(default=datetime.datetime(2020, 1, 22, 13, 22, 18, 582907, tzinfo=utc), verbose_name='shipping date'),
        ),
    ]
