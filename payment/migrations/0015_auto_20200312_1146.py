# Generated by Django 2.2.7 on 2020-03-12 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0014_auto_20200311_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendorpayment',
            name='payment_mode',
            field=models.CharField(blank=True, choices=[('cash', 'cash'), ('cheque', 'cheque')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vendorpayment',
            name='received_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]