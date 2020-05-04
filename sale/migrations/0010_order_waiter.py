# Generated by Django 2.2.7 on 2020-01-17 03:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sale', '0009_auto_20200116_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='waiter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
