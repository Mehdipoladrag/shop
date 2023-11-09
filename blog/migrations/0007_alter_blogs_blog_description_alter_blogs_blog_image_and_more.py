# Generated by Django 4.2.6 on 2023-11-03 04:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0006_alter_blogs_options_alter_category_blog_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='blog_description',
            field=models.TextField(verbose_name='توضیحات وبلاگ'),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='blog_image',
            field=models.ImageField(upload_to='blog_images/', verbose_name='عکس وبلاگ'),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='blog_name',
            field=models.CharField(max_length=100, verbose_name='نام وبلاگ'),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.category_blog', verbose_name='دسته بندی وبلاگ'),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت وبلاگ'),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='یو ار ال وبلاگ'),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='زمان ویرایش وبلاگ'),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نام کاربری'),
        ),
        migrations.AlterField(
            model_name='category_blog',
            name='name',
            field=models.CharField(max_length=100, verbose_name='نام دسته بندی'),
        ),
        migrations.AlterField(
            model_name='category_blog',
            name='slug_cat',
            field=models.SlugField(verbose_name='یو ار ال دسته بندی'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blogs', verbose_name='وبلاگ'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ساخت'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نشر دهنده توسط'),
        ),
    ]