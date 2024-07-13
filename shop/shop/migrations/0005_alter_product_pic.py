# Generated by Django 5.0.4 on 2024-07-13 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0004_rename_category_barnd_brand_category_brand"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="pic",
            field=models.ImageField(
                default=1, upload_to="images/product/%Y/%m/%d", verbose_name="عکس اصلی"
            ),
            preserve_default=False,
        ),
    ]
