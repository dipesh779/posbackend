# Generated by Django 2.2.7 on 2020-01-30 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0040_auto_20200126_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationtable',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='database.Branch'),
        ),
    ]
