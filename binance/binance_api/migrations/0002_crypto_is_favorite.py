# Generated by Django 4.1.7 on 2023-04-21 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('binance_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='crypto',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
    ]
