# Generated by Django 2.2.7 on 2020-01-28 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0092_remove_stockcomputation_sale_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.StockComputation'),
        ),
    ]
