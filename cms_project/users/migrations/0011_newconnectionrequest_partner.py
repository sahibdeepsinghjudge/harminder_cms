# Generated by Django 4.2.13 on 2025-01-15 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0010_newconnectionrequest_assigned_to"),
    ]

    operations = [
        migrations.AddField(
            model_name="newconnectionrequest",
            name="partner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.partner",
            ),
        ),
    ]
