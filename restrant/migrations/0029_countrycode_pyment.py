# Generated by Django 4.0 on 2022-08-27 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restrant', '0028_restaurantprofile_until_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='countrycode',
            name='pyment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
