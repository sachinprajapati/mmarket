# Generated by Django 3.1.5 on 2021-02-24 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0003_auto_20210127_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartline',
            name='wishlist',
            field=models.BooleanField(default=False, verbose_name='Save For Later'),
        ),
    ]
