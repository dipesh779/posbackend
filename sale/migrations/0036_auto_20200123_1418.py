# Generated by Django 2.2.7 on 2020-01-23 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0035_auto_20200122_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='seating',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='sale.Seating'),
        ),
    ]
