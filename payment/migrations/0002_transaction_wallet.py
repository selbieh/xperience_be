# Generated by Django 4.2.13 on 2024-07-14 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='wallet',
            field=models.BooleanField(default=False),
        ),
    ]
