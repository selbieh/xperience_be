# Generated by Django 4.2.13 on 2024-05-25 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_points'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='locations',
            new_name='Location',
        ),
    ]
