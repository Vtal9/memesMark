# Generated by Django 2.2.6 on 2020-04-05 11:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('searchEngine', '0003_images_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to=settings.AUTH_USER_MODEL),
        ),
    ]
