# Generated by Django 4.2.6 on 2024-03-18 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contact",
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
                ("name", models.CharField(max_length=50, verbose_name="نام")),
                ("email", models.EmailField(max_length=254, verbose_name="ایمیل")),
                ("phone", models.CharField(max_length=20, verbose_name="شماره تلفن")),
                ("subject", models.CharField(max_length=50, verbose_name="موضوع")),
                ("desc", models.TextField(verbose_name="پیام")),
            ],
            options={
                "verbose_name": "پیام",
                "verbose_name_plural": "پیام ها",
            },
        ),
    ]
