# Generated by Django 4.2.6 on 2023-11-02 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_alter_orderitem_customer_delete_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='discounted_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
