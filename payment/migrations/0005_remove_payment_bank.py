# Generated by Django 2.2.7 on 2020-01-18 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_auto_20200118_1219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='bank',
        ),
    ]
