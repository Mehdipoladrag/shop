# Generated by Django 4.2.6 on 2023-10-31 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_alter_comment_username_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='category_barnd',
        ),
        migrations.AddField(
            model_name='brand',
            name='category_barnd',
            field=models.ManyToManyField(to='shop.category'),
        ),
    ]
