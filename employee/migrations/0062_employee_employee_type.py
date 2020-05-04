# Generated by Django 2.2.7 on 2020-01-24 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0061_auto_20200124_0858'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='employee_type',
            field=models.CharField(choices=[('superadmin', 'Super Admin'), ('companyadmin', 'Company Admin'), ('BranchAdmin', 'Branch Admin'), ('staff', 'Staff')], default='staff', max_length=50),
        ),
    ]