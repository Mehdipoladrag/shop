from django.contrib import admin
from blog.models import Category_blog, Blogs, Visitor
# Register your models here.
from django.utils.translation import gettext_lazy as _



class BlogsAdmin(admin.ModelAdmin):
    list_display = ["username", "blog_name", "slug","category"]
    list_display_links = ["slug", "blog_name"]
    list_select_related = ["username","category"]
    list_filter = ["category"]
    search_fields = ["blog_name"]
    list_per_page = 10
    

    # prepopulated_fields = {"slug": ["blog_name"]} کارش اینه به صورت خودکار و همزان وقتی اسم وبلاگ رو تایپ میکنی اسلاگ میسازه
    #radio_fields = {"category": admin.VERTICAL} به صورت رادیو باتن نشون میده دسته بندی ها رو
    fieldsets = [
        (
            'مشخصات وبلاگ',
            {
            
                "fields": ["username", "blog_name", "category","slug", "blog_image","create_date","update_date"],
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

    readonly_fields = ['create_date','update_date' ]
    ordering = ["create_date"]

class CategoryBlogAdmin(admin.ModelAdmin) :
    list_display = ["name", "slug_cat"]
    search_fields = ["name"]
    list_display_links = ["name"]
    fieldsets = [
        (
            'دسته بندی وبلاگ',
            {
            
                "fields": ["name", "slug_cat"],
            },
        )
    ]

class VisitorBlogAdmin(admin.ModelAdmin) :
    list_display = ["user", "post","timestamp"]
    search_fields = ["post"]
    list_display_links = ["post"]
    readonly_fields = ["timestamp"]
admin.site.register(Blogs, BlogsAdmin)

admin.site.register(Category_blog, CategoryBlogAdmin)

admin.site.register(Visitor,VisitorBlogAdmin)