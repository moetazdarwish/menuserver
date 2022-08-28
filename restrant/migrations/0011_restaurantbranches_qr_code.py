# Generated by Django 4.0 on 2022-08-17 22:25

import django.core.validators
from django.db import migrations, models
import restrant.models


class Migration(migrations.Migration):

    dependencies = [
        ('restrant', '0010_branchesprofile_srv'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantbranches',
            name='qr_code',
            field=models.FileField(null=True, upload_to=restrant.models.branch_path, validators=[django.core.validators.FileExtensionValidator(['png', 'jpeg', 'jpg'])]),
        ),
    ]
