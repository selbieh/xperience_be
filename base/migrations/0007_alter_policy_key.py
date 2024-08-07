# Generated by Django 4.2.13 on 2024-08-07 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_policy_content_ar_policy_content_en'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policy',
            name='key',
            field=models.CharField(choices=[('privacy', 'Privacy Policy'), ('terms', 'Terms of Use'), ('cancellation', 'Cancellation Policy'), ('about', 'About Us')], max_length=20, unique=True),
        ),
    ]
