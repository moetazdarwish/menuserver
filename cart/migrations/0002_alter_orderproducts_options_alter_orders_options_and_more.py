# Generated by Django 4.0 on 2022-08-15 16:38

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderproducts',
            options={'ordering': ['-create_date']},
        ),
        migrations.AlterModelOptions(
            name='orders',
            options={'ordering': ['-create_date']},
        ),
        migrations.AddField(
            model_name='orderproducts',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='orders',
            name='note',
            field=models.TextField(blank=True, default='No Note', null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='payment_sys',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='table_no',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
