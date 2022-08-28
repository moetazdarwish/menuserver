# Generated by Django 4.0 on 2022-08-18 10:46

import django.core.validators
from django.db import migrations, models
import restrant.models


class Migration(migrations.Migration):

    dependencies = [
        ('restrant', '0014_alter_courtsbranches_qr_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='branchesprofile',
            name='is_branch',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='courtsbranches',
            name='qr_code',
            field=models.FileField(blank=True, null=True, upload_to=restrant.models.court_path, validators=[django.core.validators.FileExtensionValidator(['png', 'jpeg', 'jpg'])]),
        ),
    ]