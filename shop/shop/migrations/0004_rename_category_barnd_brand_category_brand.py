# Generated by Django 4.2.6 on 2024-03-25 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0003_alter_product_product_rate"),
    ]

    operations = [
        migrations.RenameField(
            model_name="brand",
            old_name="category_barnd",
            new_name="category_brand",
        ),
    ]
