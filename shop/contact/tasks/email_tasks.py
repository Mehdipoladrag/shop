import pytz
from celery import shared_task
from contact.models import Contact
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task(name="delete expired messages")
def delete_expired_messages():
    """
    This is a task to delete redundant messages from the database
    This task helps us keep the database lighter and cleaner from redundant data
    But it also has its disadvantages, the admin may not see the user's message in these five days
    """

    try:
        email_expired = datetime.now(tz=pytz.timezone("Asia/Tehran")) - timedelta(
            days=5
        )
        deleted_count, _ = Contact.objects.filter(created__lt=email_expired).delete()
        if deleted_count > 0:
            logger.info(f"Successfully deleted {deleted_count} expired contacts.")
        else:
            logger.info("No expired contacts found to delete.")
    except Exception as e:
        logger.error(
            f"Error occurred while deleting expired contacts: {e}", exc_info=True
        )
        raise
