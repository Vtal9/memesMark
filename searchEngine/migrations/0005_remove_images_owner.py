# Generated by Django 2.2.6 on 2020-04-05 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('searchEngine', '0004_auto_20200405_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='images',
            name='owner',
        ),
    ]
