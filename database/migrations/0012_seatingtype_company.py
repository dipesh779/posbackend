# Generated by Django 2.2.7 on 2020-01-24 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0011_auto_20200120_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='seatingtype',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seating_type', to='database.CompanyDetail'),
        ),
    ]