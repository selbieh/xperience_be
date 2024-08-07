# Generated by Django 4.2.13 on 2024-07-02 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reservations', '0010_reservation_payment_method'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('tran_ref', models.CharField(max_length=255, null=True)),
                ('response_code', models.CharField(max_length=255, null=True)),
                ('response_message', models.CharField(max_length=255, null=True)),
                ('success', models.BooleanField(default=False)),
                ('pending', models.BooleanField(default=True)),
                ('refunded', models.BooleanField(default=False)),
                ('data', models.JSONField(default=dict)),
                ('is_refund', models.BooleanField(default=False)),
                ('vat', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('fee', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='reservations.reservation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
