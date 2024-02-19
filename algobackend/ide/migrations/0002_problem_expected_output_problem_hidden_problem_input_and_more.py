# Generated by Django 5.0.2 on 2024-02-18 10:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ide", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="problem",
            name="expected_output",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="problem",
            name="hidden",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="problem",
            name="input",
            field=models.TextField(default=""),
        ),
        migrations.DeleteModel(
            name="TestCase",
        ),
    ]
