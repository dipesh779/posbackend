# Generated by Django 2.2.7 on 2020-03-12 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0017_auto_20200312_1305'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vendorpayment',
            options={},
        ),
        migrations.AddField(
            model_name='vendorpayment',
            name='created_at',
            field=models.DateField(auto_now_add=True, default='2020-01-01'),
            preserve_default=False,
        ),
    ]
