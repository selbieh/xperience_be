# Generated by Django 4.2.13 on 2024-05-31 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_subscriptionoption_delete_durationoption'),
        ('reservations', '0003_rename_dropoff_location_carreservation_dropoff_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='carreservation',
            name='subscription_option',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='car_reservations', to='services.subscriptionoption'),
        ),
    ]
