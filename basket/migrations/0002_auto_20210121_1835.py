# Generated by Django 3.1.5 on 2021-01-21 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartline',
            name='save',
        ),
        migrations.AlterField(
            model_name='cartline',
            name='price',
            field=models.FloatField(blank=True),
        ),
    ]
