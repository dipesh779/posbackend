# Generated by Django 2.2.7 on 2020-01-30 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0099_remove_purchaseorder_purchaseorder_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockcomputation',
            old_name='item_name',
            new_name='item',
        ),
    ]