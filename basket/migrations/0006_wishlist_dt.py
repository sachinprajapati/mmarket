# Generated by Django 3.1.5 on 2021-02-24 07:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0005_auto_20210224_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='dt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
