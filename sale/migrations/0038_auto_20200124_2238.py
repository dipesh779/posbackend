# Generated by Django 2.2.7 on 2020-01-24 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0037_unitofmaterial_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitofmaterial',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uom', to='database.CompanyDetail'),
        ),
    ]