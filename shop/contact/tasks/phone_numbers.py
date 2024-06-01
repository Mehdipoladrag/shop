import pytz
from celery import shared_task
from contact.models import Contact
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)



@shared_task(name='Invalid Phone Numbers')
def invalid_phone_numbers():
    try:
        phone_number = Contact.objects.exclude(phone__startswith=('09'))
        phone_number.delete()
        logger.info('Successfully deleted')

    except Exception as e:
        logger.error(f'Error occurred while deleting invalid phone numbers: {e}', exc_info=True)
        raise