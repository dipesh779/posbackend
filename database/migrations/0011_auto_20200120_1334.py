# Generated by Django 2.2.7 on 2020-01-20 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0010_auto_20200120_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactperson',
            name='vendor',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact_person', to='database.Vendor'),
        ),
    ]