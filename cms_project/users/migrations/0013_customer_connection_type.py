# Generated by Django 4.2.13 on 2025-01-23 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0012_newconnectionrequest_request_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="connection_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Internet", "Internet"),
                    ("Camera", "Camera"),
                    ("Camera+Internet", "Camera+Internet"),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]
