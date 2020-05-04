# Generated by Django 2.2.7 on 2020-01-24 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0012_seatingtype_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seatingtype',
            name='company',
        ),
        migrations.AddField(
            model_name='seatingtype',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seating_type', to='database.Branch'),
        ),
    ]
