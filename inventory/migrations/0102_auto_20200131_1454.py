# Generated by Django 2.2.7 on 2020-01-31 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0101_auto_20200131_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockcomputation',
            name='complimentory_sale',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='stockcomputation',
            name='discrepancy_stock',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='stockcomputation',
            name='expired_quantity',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='stockcomputation',
            name='final_closing_stock',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='stockcomputation',
            name='inspected_stock',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='stockcomputation',
            name='received_stock',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='stockcomputation',
            name='sale',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='stockcomputation',
            name='theoritical_QOH',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='stockcomputation',
            name='threshold_quantity',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='stockcomputation',
            name='weigh_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]
