# Generated by Django 4.2.6 on 2024-03-21 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_username'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'کاربر', 'verbose_name_plural': 'کاربر ها'},
        ),
    ]
