# Generated by Django 4.2.13 on 2024-06-08 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0007_reservation_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('WAITING_FOR_PAYMENT', 'Waiting for Payment'), ('CONFIRMED', 'Confirmed'), ('CANCELLED', 'Cancelled'), ('COMPLETED', 'Completed')], default='WAITING_FOR_PAYMENT', max_length=20),
        ),
        migrations.DeleteModel(
            name='Refund',
        ),
    ]
