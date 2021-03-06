# Generated by Django 3.1.5 on 2021-02-08 07:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pincode', models.PositiveIntegerField(validators=[django.core.validators.RegexValidator(message='Pincode number must be 6 digits long.', regex=r'^\d{6}$')])),
            ],
        ),
    ]
