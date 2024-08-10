from celery import shared_task
from datetime import datetime, timedelta
import pytz
from shop.models import Order, OrderItem, Transaction, Invoice
import logging

logger = logging.getLogger(__name__)

@shared_task(name="ClearExpiredOrdersAndRelatedData")
def clear_expired_orders_and_related_data():

    expiration_time = datetime.now(tz=pytz.timezone("Asia/Tehran")) - timedelta(seconds=30)
    
    try:

        orders_to_delete = Order.objects.filter(order_date__lt=expiration_time)
        for order in orders_to_delete:

            OrderItem.objects.filter(order=order).delete()

            Invoice.objects.filter(order=order).delete()
            Invoice.delete()
            transactions = Transaction.objects.filter(invoice__in=Invoice.objects.filter(order=order))
            transactions.delete()

            order.delete()
        
        logger.info("Expired orders and related data have been cleared successfully.")
    except Exception as e:
        logger.error(f"An error occurred while clearing expired data: {e}")