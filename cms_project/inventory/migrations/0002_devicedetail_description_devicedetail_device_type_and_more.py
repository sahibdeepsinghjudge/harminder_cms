# Generated by Django 4.2.13 on 2025-01-02 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="devicedetail",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="devicedetail",
            name="device_type",
            field=models.CharField(
                choices=[
                    ("Cable", "Cable"),
                    ("ONT Single", "ONT Single"),
                    ("ONT Dual", "ONT Dual"),
                    ("Router Single", "Router Single"),
                    ("Router Dual", "Router Dual"),
                    ("Switch", "Switch"),
                    ("Other", "Other"),
                ],
                default="Other",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="devicedetail",
            name="hsn_code",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="devicedetail",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="device_images"),
        ),
        migrations.AddField(
            model_name="devicedetail",
            name="in_stock",
            field=models.BooleanField(default=True),
        ),
    ]
