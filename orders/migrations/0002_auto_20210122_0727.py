# Generated by Django 3.1.5 on 2021-01-22 07:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='pincode',
            field=models.PositiveIntegerField(validators=[django.core.validators.RegexValidator(message='Pincode number must be 6 digits long.', regex='^(\\+\\d{1,3})?,?\\s?\\d{6}')]),
        ),
    ]
