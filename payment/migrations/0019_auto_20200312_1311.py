# Generated by Django 2.2.7 on 2020-03-12 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0018_auto_20200312_1310'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vendorpayment',
            options={'ordering': ['-payment_status', '-created_at']},
        ),
    ]
