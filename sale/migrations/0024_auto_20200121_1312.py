# Generated by Django 2.2.7 on 2020-01-21 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0011_auto_20200120_1334'),
        ('sale', '0023_invoice_bill_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='customer_name',
        ),
        migrations.AddField(
            model_name='invoice',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Customer'),
        ),
    ]
