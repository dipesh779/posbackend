# Generated by Django 2.2.7 on 2020-01-22 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0029_invoice_pay_from_debit'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Notification Table',
                'verbose_name_plural': 'Notification Tables',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
    ]