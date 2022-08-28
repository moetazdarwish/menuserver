# Generated by Django 4.0 on 2022-08-14 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restrant', '0001_initial'),
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menusname',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restrant.restaurantprofile'),
        ),
        migrations.AddField(
            model_name='menusitems',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.menuscategory'),
        ),
        migrations.AddField(
            model_name='menusitems',
            name='menu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.menusname'),
        ),
        migrations.AddField(
            model_name='branchmenu',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restrant.branchesprofile'),
        ),
        migrations.AddField(
            model_name='branchmenu',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.menuscategory'),
        ),
        migrations.AddField(
            model_name='branchesmenusitems',
            name='branch_menu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.branchmenu'),
        ),
        migrations.AddField(
            model_name='branchesmenusitems',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.menuscategory'),
        ),
        migrations.AddField(
            model_name='branchesmenusitems',
            name='menu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.menusitems'),
        ),
    ]
