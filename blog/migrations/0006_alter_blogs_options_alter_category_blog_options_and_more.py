# Generated by Django 4.2.6 on 2023-11-02 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_visitor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogs',
            options={'verbose_name': 'وبلاگ', 'verbose_name_plural': 'وبلاگ ها'},
        ),
        migrations.AlterModelOptions(
            name='category_blog',
            options={'verbose_name': 'دسته بندی وبلاگ', 'verbose_name_plural': 'دسته بندی وبلاگ ها'},
        ),
        migrations.AlterModelOptions(
            name='visitor',
            options={'verbose_name': 'بازدید کننده ', 'verbose_name_plural': 'بازدید کنندگان'},
        ),
    ]
