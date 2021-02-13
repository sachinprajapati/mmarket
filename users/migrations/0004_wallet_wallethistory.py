# Generated by Django 3.1.5 on 2021-02-13 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20210212_1412'),
        ('users', '0003_auto_20210206_1707'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bal', models.DecimalField(decimal_places=4, default=0, max_digits=12, verbose_name='Wallet Balance')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WalletHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prev_bal', models.DecimalField(decimal_places=4, max_digits=12, verbose_name='Previous Balace')),
                ('amount', models.DecimalField(decimal_places=4, max_digits=10, verbose_name='Amount Added')),
                ('dt', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orders')),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.wallet')),
            ],
        ),
    ]
