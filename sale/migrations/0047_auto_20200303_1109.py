# Generated by Django 2.2.7 on 2020-03-03 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0046_auto_20200303_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='created_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]