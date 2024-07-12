# Generated by Django 4.2.13 on 2024-07-12 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0011_carreservation_final_points_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('WAITING_FOR_PAYMENT', 'Waiting for Payment'), ('WAITING_FOR_CONFIRMATION', 'Waiting for Confirmation'), ('CONFIRMED', 'Confirmed'), ('PAID', 'Paid'), ('CANCELLED', 'Cancelled'), ('REFUNDED', 'Refunded'), ('COMPLETED', 'Completed')], default='WAITING_FOR_CONFIRMATION', max_length=25),
        ),
    ]
