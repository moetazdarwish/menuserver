# Generated by Django 4.0 on 2022-08-15 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restrant', '0002_remove_restaurantprofile_area_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='courtsbranches',
            name='tables',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
