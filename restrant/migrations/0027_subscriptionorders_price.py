# Generated by Django 4.0 on 2022-08-25 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restrant', '0026_subscriptionorders_period_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionorders',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]
