# Generated by Django 5.1.5 on 2025-01-30 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0002_apartment_is_booked'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='status',
            field=models.CharField(choices=[('living', 'Living'), ('moved_out', 'Moved Out')], default='living', max_length=15),
        ),
    ]
