# Generated by Django 2.2.7 on 2020-01-17 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0012_delete_iteminstruction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_of_order',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]