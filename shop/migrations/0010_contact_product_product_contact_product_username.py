# Generated by Django 4.2.6 on 2023-10-25 00:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_comment_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact_product',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact_product',
            name='username',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='shop.customer'),
            preserve_default=False,
        ),
    ]
