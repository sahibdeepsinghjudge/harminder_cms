# Generated by Django 4.2.13 on 2025-01-15 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0009_newconnectionrequest_alter_customer_addhar_number_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="newconnectionrequest",
            name="assigned_to",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.technician",
            ),
        ),
    ]
