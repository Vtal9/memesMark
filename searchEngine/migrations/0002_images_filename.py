# Generated by Django 2.2.6 on 2020-04-03 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchEngine', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='fileName',
            field=models.TextField(blank=True, null=True),
        ),
    ]
