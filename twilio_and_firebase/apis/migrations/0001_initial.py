# Generated by Django 5.1.5 on 2025-01-28 16:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TwilioCredentials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_sid', models.CharField(max_length=255)),
                ('auth_token', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='twilio_credentials', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Twilio Credentials',
                'verbose_name_plural': 'Twilio Credentials',
            },
        ),
    ]
