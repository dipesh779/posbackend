# Generated by Django 2.2.7 on 2020-01-21 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0024_auto_20200121_1312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='discount_from_reward',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment',
        ),
    ]
