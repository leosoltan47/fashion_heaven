# Generated by Django 5.1.7 on 2025-03-27 22:58

import pages.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0004_alter_productdetails_color_code"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productdetails",
            name="color_code",
        ),
        migrations.CreateModel(
            name="Color",
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
                (
                    "color_code",
                    models.CharField(
                        default="#FF0000",
                        max_length=9,
                        validators=[pages.models.validate_hex_color],
                    ),
                ),
                ("images", models.ManyToManyField(to="pages.productimages")),
            ],
        ),
    ]
