# Generated by Django 2.2.7 on 2020-03-11 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0020_companydetail_company_logo'),
        ('payment', '0011_auto_20200311_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorpayment',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='database.Branch'),
            preserve_default=False,
        ),
    ]