# Generated by Django 3.1.5 on 2021-02-15 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20210212_1412'),
        ('users', '0004_wallet_wallethistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallethistory',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.orders'),
        ),
    ]