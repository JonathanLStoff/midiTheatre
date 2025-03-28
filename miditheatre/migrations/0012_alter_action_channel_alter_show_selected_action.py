# Generated by Django 5.1.5 on 2025-02-07 00:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("miditheatre", "0011_alter_action_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="action",
            name="channel",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(15),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="show",
            name="selected_action",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
