# Generated by Django 2.2.7 on 2020-01-19 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0017_auto_20200118_1248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='additional_discount',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='card_bill_number',
        ),
    ]
