# Generated by Django 2.2.7 on 2020-01-21 05:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0047_auto_20200120_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='purchase_order_date',
            field=models.DateField(default=datetime.datetime(2020, 1, 21, 5, 53, 46, 75314, tzinfo=utc), verbose_name='purchase order date'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='shipping_date',
            field=models.DateField(default=datetime.datetime(2020, 1, 21, 5, 53, 46, 75449, tzinfo=utc), verbose_name='shipping date'),
        ),
    ]
