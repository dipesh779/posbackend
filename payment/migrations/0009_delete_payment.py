# Generated by Django 2.2.7 on 2020-01-21 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0025_auto_20200121_1538'),
        ('payment', '0008_auto_20200121_1312'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
    ]