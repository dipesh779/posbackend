# Generated by Django 2.2.7 on 2020-01-22 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0034_auto_20200122_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationtable',
            name='seating_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='notificationtable',
            name='waiter_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='notificationtable',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Branch'),
        ),
        migrations.AlterField(
            model_name='notificationtable',
            name='message',
            field=models.CharField(max_length=255, null=True),
        ),
    ]