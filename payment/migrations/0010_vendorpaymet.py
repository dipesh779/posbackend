# Generated by Django 2.2.7 on 2020-03-11 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0119_auto_20200310_1255'),
        ('payment', '0009_delete_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorPaymet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.CharField(choices=[('paid', 'paid'), ('unpaid', 'unpaid')], default='unpaid', max_length=100)),
                ('bill_of_stock', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inventory.BillOfStock')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Vendor')),
            ],
        ),
    ]