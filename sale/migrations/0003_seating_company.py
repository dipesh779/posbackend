# Generated by Django 2.2.7 on 2020-01-15 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_auto_20200115_1301'),
        ('sale', '0002_auto_20200115_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='seating',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='database.CompanyDetail'),
        ),
    ]
