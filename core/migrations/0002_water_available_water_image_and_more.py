# Generated by Django 4.1.5 on 2023-01-30 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="water",
            name="available",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="water",
            name="image",
            field=models.ImageField(blank=True, upload_to="products/%Y/%m/%d"),
        ),
        migrations.AddIndex(
            model_name="water",
            index=models.Index(fields=["name"], name="core_water_name_bdb1a8_idx"),
        ),
    ]