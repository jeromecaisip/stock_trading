# Generated by Django 3.0.9 on 2020-08-13 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='trade_at',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Current stock price when order was made'),
        ),
    ]
