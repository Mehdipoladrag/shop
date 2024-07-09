from django.contrib import admin
from .models import Category_blog, Blogs, Visitor  # Changed import path to relative


class BlogsAdmin(admin.ModelAdmin):
    list_display = ["username", "blog_name", "slug", "category", "create_date", "update_date"]  # Added create_date and update_date to list_display
    list_display_links = ["blog_name", "slug"]  # Changed list_display_links order
    list_select_related = ["username", "category"]
    list_filter = ["category"]
    search_fields = ["blog_name"]
    list_per_page = 10
    prepopulated_fields = {"slug": ("blog_name",)}  # Fixed prepopulated_fields syntax
    radio_fields = {"category": admin.VERTICAL}  # Added radio_fields example

    fieldsets = [
        (
            "مشخصات وبلاگ",
            {
                "fields": [
                    "username",
                    "blog_name",
                    "category",
                    "slug",
                    "blog_image",
                    ("create_date", "update_date"),  # Grouped create_date and update_date
                ],
            },
        ),
        (
            "متن وبلاگ",
            {
                "classes": ["wide"],
                "fields": ["blog_description"],
            },
        ),
    ]
    readonly_fields = ["create_date", "update_date"]
    ordering = ["-create_date"]  # Changed ordering to descending order of create_date


class CategoryBlogAdmin(admin.ModelAdmin):
    list_display = ["name", "slug_cat"]
    search_fields = ["name"]
    list_display_links = ["name"]
    fieldsets = [
        (
            "دسته بندی وبلاگ",
            {
                "fields": ["name", "slug_cat"],
            },
        )
    ]


class VisitorBlogAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "timestamp"]
    search_fields = ["post"]
    list_display_links = ["post"]
    readonly_fields = ["timestamp"]


admin.site.register(Blogs, BlogsAdmin)
admin.site.register(Category_blog, CategoryBlogAdmin)  # Changed Category_blog to CategoryBlogAdmin
admin.site.register(Visitor, VisitorBlogAdmin)
