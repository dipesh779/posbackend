# Generated by Django 2.2.7 on 2020-01-18 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_remove_payment_bank'),
        ('sale', '0015_auto_20200118_1118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='bank',
        ),
        migrations.DeleteModel(
            name='Bank',
        ),
    ]