# Generated by Django 4.0 on 2022-08-21 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0004_orders_is_rate_orders_rate_orders_tran_ref'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('restrant', '0018_alter_restaurantprofile_vat'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('status', models.CharField(blank=True, max_length=20, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restrant.branchesprofile')),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.costumerprofile')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.orders')),
                ('restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restrant.restaurantprofile')),
            ],
        ),
        migrations.CreateModel(
            name='NotifUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False, null=True)),
                ('title', models.CharField(blank=True, max_length=20, null=True)),
                ('body', models.CharField(blank=True, max_length=20, null=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]