# Generated by Django 4.0 on 2022-08-16 18:57

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restrant', '0008_alter_restaurantbranches_table_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='branchesprofile',
            name='service',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='restaurantprofile',
            name='service',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='restaurantprofile',
            name='tax',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='restaurantprofile',
            name='vat',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
