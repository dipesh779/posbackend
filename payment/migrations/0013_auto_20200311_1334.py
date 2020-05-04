# Generated by Django 2.2.7 on 2020-03-11 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0012_vendorpayment_branch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendorpayment',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Branch'),
        ),
    ]
