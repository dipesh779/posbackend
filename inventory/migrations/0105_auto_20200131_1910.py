# Generated by Django 2.2.7 on 2020-01-31 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0104_menuitemcosting_cost_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitemcosting',
            name='cost_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
