# Generated by Django 2.2.7 on 2020-01-21 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0025_auto_20200121_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='customer_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
