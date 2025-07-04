# Generated by Django 5.1.7 on 2025-05-02 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0006_remove_products_details_productdetails_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="collections",
            name="badge",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="collections",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="collections",
            name="name",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
