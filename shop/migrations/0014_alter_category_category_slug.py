# Generated by Django 4.2.6 on 2023-10-26 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_category_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_slug',
            field=models.SlugField(unique=True, verbose_name='Category slug'),
        ),
    ]