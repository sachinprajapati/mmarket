# Generated by Django 3.1.5 on 2021-01-20 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_mrp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattributevalue',
            name='attribute',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.productattribute', verbose_name='Attribute'),
        ),
    ]
