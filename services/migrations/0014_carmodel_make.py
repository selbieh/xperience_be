# Generated by Django 4.2.13 on 2024-06-27 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0013_alter_hotelservice_features'),
    ]

    operations = [
        migrations.AddField(
            model_name='carmodel',
            name='make',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, related_name='car_model', to='services.carmake'),
        ),
    ]
