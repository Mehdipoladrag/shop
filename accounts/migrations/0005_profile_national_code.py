# Generated by Django 4.2.6 on 2023-10-27 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_profile_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='national_code',
            field=models.CharField(default=1, max_length=10, verbose_name='کد ملی'),
            preserve_default=False,
        ),
    ]
