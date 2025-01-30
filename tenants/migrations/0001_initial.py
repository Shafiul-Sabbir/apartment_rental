# Generated by Django 5.1.5 on 2025-01-30 04:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=15)),
                ('move_in_date', models.DateField()),
                ('move_out_date', models.DateField(blank=True, null=True)),
                ('apartment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tenants.apartment')),
            ],
        ),
    ]
