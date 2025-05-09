# Generated by Django 5.1.5 on 2025-02-07 21:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0005_alter_tenant_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='apartment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenants.apartment'),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='status',
            field=models.CharField(choices=[('will_arrive', 'Will Arrive'), ('living', 'Living'), ('moved_out', 'Moved Out')], max_length=15),
        ),
    ]
