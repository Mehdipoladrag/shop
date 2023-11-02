# Generated by Django 4.2.6 on 2023-10-27 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_profile_shomare_shaba'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='state',
        ),
        migrations.AddField(
            model_name='profile',
            name='street',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='street'),
        ),
    ]
