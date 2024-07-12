# Generated by Django 4.2.13 on 2024-07-12 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0010_reservation_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='carreservation',
            name='final_points_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='hotelreservation',
            name='final_points_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('WAITING_FOR_PAYMENT', 'Waiting for Payment'), ('WAITING_FOR_CONFIRMATION', 'Waiting for Confirmation'), ('CONFIRMED', 'Confirmed'), ('PAID', 'Paid'), ('CANCELLED', 'Cancelled'), ('REFUNDED', 'Refunded'), ('COMPLETED', 'Completed')], default='WAITING_FOR_PAYMENT', max_length=25),
        ),
    ]
