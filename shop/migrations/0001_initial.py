# Generated by Django 4.2.6 on 2023-10-24 15:50

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=50, verbose_name='Brand Name')),
                ('brand_code', models.IntegerField(verbose_name='Brand_code')),
                ('brand_pic', models.ImageField(blank=True, null=True, upload_to='images/brand/%Y/%m/%d', verbose_name='Brand Image')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, verbose_name='Category')),
                ('category_code', models.IntegerField(verbose_name='Category Code')),
                ('category_pic', models.ImageField(blank=True, null=True, upload_to='images/category/%Y/%m/%d', verbose_name='Category Image')),
            ],
        ),
        migrations.CreateModel(
            name='Contact_product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_product', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_code', models.IntegerField(verbose_name='Code')),
                ('first_name', models.CharField(max_length=20, verbose_name='Name')),
                ('last_name', models.CharField(max_length=20, verbose_name='Family')),
                ('address', models.TextField(verbose_name='Address')),
                ('zipcode', models.CharField(max_length=20, verbose_name='Zip Code')),
                ('state', models.CharField(max_length=20, verbose_name='State')),
                ('city', models.CharField(max_length=20, verbose_name='City')),
                ('mobile', models.CharField(max_length=20, verbose_name='Mobile')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('age', models.PositiveIntegerField(verbose_name='Age')),
                ('gender', models.BooleanField(default=False, verbose_name='Gender')),
                ('shomare_shaba', models.IntegerField(verbose_name='shomare_shaba')),
                ('shomare_cart', models.IntegerField(verbose_name='shomare_cart')),
                ('back_money', models.CharField(default='شماره شبا', max_length=50, verbose_name='Back money')),
                ('customer_image', models.ImageField(blank=True, null=True, upload_to='images/userimage/%Y/%m/%d', verbose_name='User Image')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_info', models.TextField(verbose_name='Info Product')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_date', models.DateTimeField(auto_now_add=True)),
                ('authority', models.CharField(blank=True, max_length=50, null=True, verbose_name='Authority')),
            ],
        ),
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.CharField(max_length=50, verbose_name='Offer Name')),
                ('offer_pic', models.ImageField(blank=True, null=True, upload_to='images/offer/%Y/%m/%d', verbose_name='Offer Image')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True, verbose_name='Order Date')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=1, max_digits=10, verbose_name='amount')),
                ('status', models.CharField(choices=[('pending', 'انتظار'), ('failed', 'ناموفق'), ('completed', 'تکمیل شده')], default='pending', max_length=50, verbose_name='Status')),
                ('invoice', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.invoice')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.IntegerField(verbose_name='Product Code')),
                ('product_name', models.CharField(max_length=20, verbose_name='Product Name')),
                ('product_color', models.CharField(max_length=20, verbose_name='Color')),
                ('product_number', models.PositiveIntegerField(verbose_name='Product Number')),
                ('capability', models.CharField(max_length=20, verbose_name='capability Name')),
                ('resolution', models.IntegerField(verbose_name='Resolution')),
                ('technology', models.CharField(max_length=50, verbose_name='technology')),
                ('platform_os', models.CharField(max_length=50, verbose_name='Os')),
                ('bluetooth', models.CharField(choices=[('دارد', 'دارد'), ('ندارد', 'ندارد')], default=False, max_length=20, verbose_name='Bluetooth')),
                ('product_rate', models.IntegerField(verbose_name='Rate')),
                ('specifications', models.TextField(verbose_name='Specifictaion')),
                ('product_description', models.TextField(verbose_name='Description')),
                ('mini_description', models.CharField(max_length=50, verbose_name='Mini Description')),
                ('price', models.DecimalField(decimal_places=1, max_digits=10, verbose_name='Product Price')),
                ('offer', models.IntegerField(blank=True, null=True, verbose_name='offer')),
                ('time_send', models.PositiveIntegerField(verbose_name='Time Send')),
                ('pic', models.ImageField(blank=True, null=True, upload_to='images/product/%Y/%m/%d', verbose_name='Image')),
                ('pic2', models.ImageField(blank=True, null=True, upload_to='images/product/productimage/%Y/%m/%d', verbose_name='Image2')),
                ('pic3', models.ImageField(blank=True, null=True, upload_to='images/product/productimage/%Y/%m/%d', verbose_name='Image3')),
                ('pic4', models.ImageField(blank=True, null=True, upload_to='images/product/productimage/%Y/%m/%d', verbose_name='Image4')),
                ('pic5', models.ImageField(blank=True, null=True, upload_to='images/product/productimage/%Y/%m/%d', verbose_name='Image5')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Update At')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=models.CharField(max_length=20, verbose_name='Product Name'))),
                ('product_brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.brand', verbose_name='Brand')),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category', verbose_name='Category')),
                ('product_inf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.info', verbose_name='Info')),
                ('product_offer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.offers', verbose_name='Offers')),
            ],
            options={
                'ordering': ('create_date',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_price', models.DecimalField(decimal_places=1, max_digits=10, verbose_name='Product Price')),
                ('product_count', models.PositiveIntegerField(verbose_name='Product Count')),
                ('product_cost', models.DecimalField(decimal_places=1, max_digits=10, verbose_name='Product cost')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.customer')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.product')),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.order'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('rate', models.PositiveIntegerField(default=False)),
                ('created_date', models.DateTimeField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.customer')),
            ],
        ),
        migrations.AddField(
            model_name='brand',
            name='category_barnd',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category', verbose_name='Category'),
        ),
    ]
