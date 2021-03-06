# Generated by Django 4.0.3 on 2022-03-03 16:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='quantity',
            field=models.PositiveBigIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Cantidad'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Precio'),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveBigIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Unidades disponibles'),
        ),
    ]
