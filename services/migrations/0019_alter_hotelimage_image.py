# Generated by Django 4.2.13 on 2024-06-30 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0018_hotelservice_points_subscriptionoption_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelimage',
            name='image',
            field=models.FileField(upload_to='hotel_images/'),
        ),
    ]
