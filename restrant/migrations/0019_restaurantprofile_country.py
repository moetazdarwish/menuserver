# Generated by Django 4.0 on 2022-08-24 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restrant', '0018_alter_restaurantprofile_vat'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantprofile',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
