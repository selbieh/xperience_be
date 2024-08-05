# Generated by Django 4.2.13 on 2024-08-05 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0022_alter_hotelservice_points_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelservice',
            name='dollar_day_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='hotelservicefeature',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='feat_icon/'),
        ),
        migrations.AddField(
            model_name='serviceoption',
            name='dollar_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='subscriptionoption',
            name='dollar_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
