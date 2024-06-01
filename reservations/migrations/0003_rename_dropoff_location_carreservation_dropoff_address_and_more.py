# Generated by Django 4.2.13 on 2024-05-31 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carreservation',
            old_name='dropoff_location',
            new_name='dropoff_address',
        ),
        migrations.RenameField(
            model_name='carreservation',
            old_name='pickup_location',
            new_name='pickup_address',
        ),
        migrations.RenameField(
            model_name='hotelreservation',
            old_name='location',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='carreservation',
            name='final_price',
        ),
        migrations.RemoveField(
            model_name='carreservation',
            name='type',
        ),
        migrations.RemoveField(
            model_name='carreservationoption',
            name='final_price',
        ),
        migrations.RemoveField(
            model_name='hotelreservation',
            name='final_price',
        ),
        migrations.RemoveField(
            model_name='hotelreservationoption',
            name='final_price',
        ),
        migrations.AddField(
            model_name='carreservation',
            name='dropoff_lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='carreservation',
            name='dropoff_long',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='carreservation',
            name='dropoff_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='carreservation',
            name='pickup_lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='carreservation',
            name='pickup_long',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='carreservation',
            name='pickup_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='hotelreservation',
            name='location_lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hotelreservation',
            name='location_long',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hotelreservation',
            name='location_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]