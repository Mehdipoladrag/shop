from django.contrib import admin
from accounts.models import CustomUser, CustomProfileModel
from accounts.permissions import AdminPermission

#


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "date_joined",
    )
    list_display_links = (
        "username",
        "email",
    )

    search_fields = ["first_name", "last_name", "username"]
    list_filter = (
        "is_staff",
        "date_joined",
    )
    list_per_page = 10
    readonly_fields = (
        "id",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "password",
        "date_joined",
        "last_login",
    )
    # FieldSets
    fieldsets = (
        (
            "اطلاعات کاربری",
            {
                "fields": (
                    "id",
                    "username",
                    "first_name",
                    "last_name",
                    "is_staff",
                    "password",
                ),
            },
        ),
        (
            "اطلاعات ورود و خروج",
            {
                "fields": (
                    "date_joined",
                    "last_login",
                )
            },
        ),
    )
    # Permissions
    permissions_class = AdminPermission


class CustomProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id_obj",
        "user",
        "national_code",
        "is_complete",
    )
    list_display_links = ("user",)
    list_filter = ("age", "gender", "city", "is_complete")
    search_fields = ("age", "gender", "city", "is_complete")
    list_per_page = 10
    readonly_fields = [
        "user",
        "national_code",
        "age",
        "gender",
        "mobile",
        "customer_image",
        "is_complete",
        "card_number",
        "iban",
        "back_money",
        "address",
        "zipcode",
        "street",
        "city",
    ]
    # FieldSets
    fieldsets = (
        (
            "اطلاعات کاربری",
            {
                "fields": (
                    "user",
                    "national_code",
                    "age",
                    "gender",
                    "mobile",
                    "is_complete",
                    "customer_image",
                )
            },
        ),
        ("اطلاعات بانکی", {"fields": ("card_number", "iban", "back_money")}),
        (
            "اطلاعات آدرس",
            (
                {
                    "fields": (
                        "zipcode",
                        "street",
                        "city",
                        "address",
                    )
                }
            ),
        ),
    )

    permissions_class = AdminPermission

    # id obj From CustomUser
    def id_obj(self, obj):
        return obj.user.id

    id_obj.short_description = "id کاربر"


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CustomProfileModel, CustomProfileAdmin)
