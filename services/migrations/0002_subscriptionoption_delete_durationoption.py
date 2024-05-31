# Generated by Django 4.2.13 on 2024-05-31 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('type', models.CharField(choices=[('RIDE', 'Ride'), ('TRAVEL', 'Travel'), ('AIRPORT', 'Airport')], max_length=50)),
                ('duration_hours', models.IntegerField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('car_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription_options', to='services.carservice')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='DurationOption',
        ),
    ]
