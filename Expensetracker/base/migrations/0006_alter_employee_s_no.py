# Generated by Django 5.0.2 on 2024-06-20 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_employee_contract_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='s_no',
            field=models.IntegerField(),
        ),
    ]
