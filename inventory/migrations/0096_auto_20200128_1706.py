# Generated by Django 2.2.7 on 2020-01-28 11:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0095_stock_threshold_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockcomputation',
            name='unit_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='unit price'),
        ),
        migrations.AlterField(
            model_name='stockcomputation',
            name='uom',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='uom'),
        ),
    ]