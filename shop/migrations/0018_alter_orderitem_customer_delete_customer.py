# Generated by Django 4.2.6 on 2023-11-02 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0017_alter_orderitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
