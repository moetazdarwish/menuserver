# Generated by Django 4.0 on 2022-08-27 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0008_alter_branchrate_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertracking',
            name='process_date',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
