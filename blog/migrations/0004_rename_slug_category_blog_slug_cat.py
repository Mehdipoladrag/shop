# Generated by Django 4.2.6 on 2023-10-26 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_category_blog_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category_blog',
            old_name='slug',
            new_name='slug_cat',
        ),
    ]
