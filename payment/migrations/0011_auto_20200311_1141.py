# Generated by Django 2.2.7 on 2020-03-11 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0119_auto_20200310_1255'),
        ('payment', '0010_vendorpaymet'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VendorPaymet',
            new_name='VendorPayment',
        ),
    ]
