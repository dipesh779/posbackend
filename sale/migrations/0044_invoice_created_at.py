# Generated by Django 2.2.7 on 2020-03-02 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0043_merge_20200217_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='created_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
