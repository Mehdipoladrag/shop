# Generated by Django 4.2.6 on 2023-11-21 22:25

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_blogs_blog_description_alter_blogs_blog_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='create_date',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='زمان ساخت وبلاگ'),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='update_date',
            field=django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='زمان ویرایش وبلاگ'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='timestamp',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ساخت'),
        ),
    ]
