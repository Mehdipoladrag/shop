from celery import shared_task
from datetime import datetime, timedelta
from decimal import Decimal
import pytz
import logging

from shop.models import (
    Order, OrderItem, 
    Transaction, Invoice, 
    Product, Brand, Category
)


logger = logging.getLogger(__name__)

@shared_task(name="Clear Expired Orders And Related Data")
def ClearExpiredOrdersRelatedData():
    """
        This is a Task for orders which 
        Orders and Transaction Expired And We need 
        To Remove this Orders.
    """

    expiration_time = datetime.now(tz=pytz.timezone("Asia/Tehran")) - timedelta(seconds=30)
    
    try:
        
        orders_to_delete = Order.objects.filter(order_date__lt=expiration_time)
        
        for order in orders_to_delete:
            OrderItem.objects.filter(order=order).delete()
            invoices_to_delete = Invoice.objects.filter(order=order)
            for invoice in invoices_to_delete:
                Transaction.objects.filter(invoice=invoice).delete()
                invoice.delete()
            order.delete()
        logger.info("Expired orders and related data have been cleared successfully.")
    except Exception as e:
        logger.error(f"An error occurred while clearing expired data: {e}")
    finally: 
        logger.error(f"Data Not found")


@shared_task(name="Clear Product Astronomical Price (**Args)")
def ClearProductAstronomicalPrice(price_threshold='50000000'):
    """
        This is a Task for orders which 
        Products Astronomical Price And We need 
        To Remove this Products.
    """
    try:
        price_threshold = Decimal(price_threshold)
        products_delete = Product.objects.filter(price__gt=price_threshold) # We Should add a Argument For this Task in panel Admin
        count = products_delete.count()

        if count > 0:
            products_delete.delete()
            logger.info(f"Products with very high prices have been successfully removed. The number was deleted: {count}.")
        else:
            logger.info("No products found with too high a price to remove.")

    except Exception as e:
        logger.error(f"An error occurred while clearing data: {e}")



@shared_task(name = "Manage Brands Code(**Args)")
def ManageBrandCode(code="12"):
    """
        This is a Task for Manage a Brands Code which 
        Codes not in Shop And We need 
        To Remove this Brands.
    """
    try: 
        brand_code = Brand.objects.filter(brand_code__gt = code) # We Should add a Argument For this Task in panel Admin
        count_data = brand_code.count()
        if count_data > 0 : 
            brand_code.delete()
            logger.info(f"Brands have been successfully removed. The number was deleted: {count_data}.")
    except Exception as e: 
        logger.error(f"Error: {e}")         


@shared_task(name = "Manage Category Code(**Args)")
def ManageCategoryCode(code="12"):
    """
        This is a Task for Manage a Category Code which 
        Codes not in Shop And We need 
        To Remove this Category.
    """
    try: 
        category_code = Category.objects.filter(category_code__gt = code) # We Should add a Argument For this Task in panel Admin
        count_data = category_code.count()
        if count_data > 0 : 
            category_code.delete()
            logger.info(f"Category have been successfully removed. The number was deleted: {count_data}.")
    except Exception as e: 
        logger.error(f"Error: {e}")    