# Generated by Django 4.2.13 on 2024-07-02 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0009_delete_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='payment_method',
            field=models.CharField(choices=[('CREDIT_CARD', 'Credit Card'), ('WALLET', 'Wallet'), ('CASH_ON_DELIVERY', 'Cash on Delivery'), ('CAR_POS', 'Car Point of Sale'), ('POINTS', 'Points')], default='CASH_ON_DELIVERY', max_length=20),
        ),
    ]
