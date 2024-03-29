# Generated by Django 2.2.7 on 2020-01-29 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0097_auto_20200131_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billofstock',
            name='additional_discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4, verbose_name='additional discount(%)'),
        ),
        migrations.AlterField(
            model_name='billofstockitem',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4, verbose_name='discount(%)'),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4, verbose_name='discount(%)'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='additional_discount_percentage',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4, verbose_name='additional discount(%)'),
        ),
    ]
