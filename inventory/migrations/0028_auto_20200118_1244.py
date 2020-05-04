# Generated by Django 2.2.7 on 2020-01-18 06:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0027_auto_20200118_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='purchase_order_date',
            field=models.DateField(default=datetime.datetime(2020, 1, 18, 6, 59, 29, 683408, tzinfo=utc), verbose_name='purchase order date'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='shipping_date',
            field=models.DateField(default=datetime.datetime(2020, 1, 18, 6, 59, 29, 683506, tzinfo=utc), verbose_name='shipping date'),
        ),
    ]
