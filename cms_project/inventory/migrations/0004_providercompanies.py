# Generated by Django 4.2.13 on 2025-01-22 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0003_attacheddevice"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProviderCompanies",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("short_name", models.CharField(max_length=255)),
                (
                    "provider_type",
                    models.CharField(
                        choices=[(1, "ISP"), (2, "Camera Connection")], max_length=255
                    ),
                ),
            ],
        ),
    ]
