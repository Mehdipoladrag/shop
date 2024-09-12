from celery import shared_task
from blog.models import Blogs
from accounts.models import CustomUser
import logging

logger = logging.getLogger(__name__)


@shared_task(name="Delete blogs without admin permission")
def DeleteUserBlogWithOutPermissions():
    """
    This is a task to delete blogs of users who do not have
    permission to access the blog page and create a blog
    """
    try:
        non_admin_users = CustomUser.objects.filter(is_superuser=False)
        for user in non_admin_users:
            blog_data = Blogs.objects.filter(username=user.username)
            blog_data.delete()
    except Exception as e:
        logger.error(f"Error: Something went wrong {e}")


@shared_task(name="Manage Image Size")
def manage_image_size(size_limit_kb=200):
    """
    Task to delete images larger than a specified size.
    """
    try:
        size_limit_bytes = int(size_limit_kb) * 1024
        blogs = Blogs.objects.all()
        for blog in blogs:
            if blog.blog_image:
                image_size = blog.blog_image.size
                if image_size > size_limit_bytes:
                    blog.blog_image.delete()  # Delete the image file
                    blog.delete()  # Delete the blog entry
                    logger.info(
                        f"Deleted image for blog ID {blog.id} & {blog.blog_name} due to size exceeding {size_limit_kb} kb."
                    )
    except Exception as e:
        logger.error(f"Error: We have an error {e}")
