# Generated by Django 2.2.7 on 2020-01-18 07:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0029_auto_20200118_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='purchase_order_date',
            field=models.DateField(default=datetime.datetime(2020, 1, 18, 7, 3, 32, 269672, tzinfo=utc), verbose_name='purchase order date'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='shipping_date',
            field=models.DateField(default=datetime.datetime(2020, 1, 18, 7, 3, 32, 269776, tzinfo=utc), verbose_name='shipping date'),
        ),
    ]
