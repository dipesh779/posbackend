# Generated by Django 2.2.7 on 2020-01-26 12:56

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0040_auto_20200126_1249'),
        ('database', '0013_auto_20200124_1551'),
        ('inventory', '0089_auto_20200126_1829'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillOfStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('invoice_number', models.PositiveIntegerField(verbose_name='invoice number')),
                ('shipping_charge', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('additional_discount', models.DecimalField(blank=True, decimal_places=0, max_digits=2, null=True, verbose_name='additional discount(%)')),
                ('vat', models.BooleanField(default=False)),
                ('tax', models.BooleanField(default=False)),
                ('final_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('payment_mode', models.CharField(blank=True, choices=[('cash', 'Cash'), ('credit', 'Credit')], max_length=100, null=True)),
                ('credit_date', models.DateField(blank=True, null=True)),
                ('payment_terms', models.CharField(blank=True, max_length=100, null=True, verbose_name='payment terms')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Branch')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='purchaseitem',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='purchaseorder',
            options={'ordering': ['id']},
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='payment_terms',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='purchase_order_date',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='purchase_order_number',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='shipping_term',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='vendor_id',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='vendor_name',
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='branch',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='database.Branch'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='purchaseorder_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='vendor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='database.Vendor', verbose_name='vendor'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='amount'),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3, verbose_name='discount(%)'),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='quantity'),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='unit price'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Cash'), ('credit', 'Credit')], default=None, help_text='choose your payment method', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='shipping_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='shipping date'),
        ),
        migrations.CreateModel(
            name='StockComputation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('item_name', models.CharField(max_length=100)),
                ('uom', models.CharField(max_length=100, verbose_name='uom')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='unit price')),
                ('opening_stock', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('received_stock', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('sale', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('sale_quantity', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('complimentory_sale', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('expired_quantity', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('theoritical_QOH', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('inspected_stock', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('discrepancy_stock', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('final_closing_stock', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('weigh_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('threshold_quantity', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Branch')),
            ],
            options={
                'verbose_name_plural': 'stock computation',
                'get_latest_by': 'created_at',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('item', models.CharField(max_length=100)),
                ('uom', models.CharField(max_length=100)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=100)),
                ('stock_quantity', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('weigh_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Branch')),
            ],
            options={
                'verbose_name_plural': 'Stock',
            },
        ),
        migrations.CreateModel(
            name='MenuItemCosting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selling_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='set selling price')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Branch')),
                ('menu_category_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='menu', to='sale.MenuItem')),
            ],
        ),
        migrations.CreateModel(
            name='ItemsForMenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_used', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('partial_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Stock')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='inventory.MenuItemCosting')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=100)),
                ('uom', models.CharField(max_length=100)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='BillOfStockItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(blank=True, max_length=100, null=True, verbose_name='item')),
                ('uom', models.CharField(blank=True, max_length=100, null=True, verbose_name='uom')),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='unit price')),
                ('ordered_quantity', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('received_quantity', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('quantity_not_received', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=3, verbose_name='discount(%)')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('bill_of_stock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='inventory.BillOfStock')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='billofstock',
            name='purchase_order',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.PurchaseOrder', verbose_name='purchase order'),
        ),
        migrations.AddField(
            model_name='billofstock',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Vendor'),
        ),
    ]
