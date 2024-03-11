# Generated by Django 5.0.2 on 2024-02-20 11:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ide", "0002_alter_problem_languages_supported_testcaseresult"),
    ]

    operations = [
        migrations.AddField(
            model_name="testcase",
            name="question",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to="ide.problem",
            ),
            preserve_default=False,
        ),
    ]