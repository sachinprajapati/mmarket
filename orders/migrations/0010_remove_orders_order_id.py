# Generated by Django 3.1.5 on 2021-05-12 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20210212_1412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='order_id',
        ),
    ]