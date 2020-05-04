# Generated by Django 2.2.7 on 2020-01-21 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0011_auto_20200120_1334'),
        ('payment', '0007_remove_payment_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='customer_name',
        ),
        migrations.AddField(
            model_name='payment',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Customer'),
        ),
    ]
