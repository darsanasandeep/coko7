# Generated by Django 4.2.3 on 2023-07-21 08:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("task", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserTask",
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
                ("task_name", models.CharField(max_length=20)),
                ("start_date", models.DateField()),
                ("due_date", models.DateField()),
                ("discrp", models.CharField(max_length=100)),
                ("status", models.CharField(max_length=10)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
