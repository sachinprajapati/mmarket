# Generated by Django 3.1.5 on 2021-02-06 11:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to=settings.AUTH_USER_MODEL),
        ),
    ]
