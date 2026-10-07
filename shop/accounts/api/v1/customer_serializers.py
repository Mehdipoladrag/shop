import re

from django.contrib.auth import authenticate
from rest_framework import serializers

from accounts.models import CustomProfileModel, CustomUser
from shop.models import Order

MIN_PASSWORD_LENGTH = 8
USERNAME_PREFIX = "@"

FIELD_MESSAGES = {
    "required": "لطفاً این فیلد را پر کنید",
    "blank": "لطفاً این فیلد را پر کنید",
    "null": "لطفاً این فیلد را پر کنید",
    "invalid": "مقدار واردشده معتبر نیست",
}


class PersianMessagesMixin:
    """Replaces DRF's English default field errors with the Persian ones of the old forms."""

    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            for key, message in FIELD_MESSAGES.items():
                if key in field.error_messages:
                    field.error_messages[key] = message
        return fields


def validate_new_password(value):
    if len(value) < MIN_PASSWORD_LENGTH:
        raise serializers.ValidationError("رمز عبور باید حداقل ۸ کاراکتر باشد.")
    return value


class RegisterSerializer(PersianMessagesMixin, serializers.Serializer):
    """Same rules as the old registration form."""

    username = serializers.CharField(max_length=25)
    email = serializers.EmailField(error_messages={"invalid": "لطفاً یک ایمیل معتبر وارد کنید"})
    first_name = serializers.CharField(max_length=25)
    last_name = serializers.CharField(max_length=25)
    password1 = serializers.CharField(max_length=128, write_only=True, trim_whitespace=False)
    password2 = serializers.CharField(max_length=128, write_only=True, trim_whitespace=False)

    def validate_username(self, value):
        if value[0].isdigit():
            raise serializers.ValidationError("نام کاربری نمی‌تواند با عدد شروع شود")
        if not value.startswith(USERNAME_PREFIX):
            raise serializers.ValidationError("نام کاربری باید با @ شروع شود")
        if CustomUser.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("نام کاربری تکراری است")
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("ایمیل تکراری است")
        return value

    def validate_password1(self, value):
        return validate_new_password(value)

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError({"password2": "رمزهای عبور مطابقت ندارند."})
        return attrs

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password1"])
        user.save()
        CustomProfileModel.objects.create(user=user)
        return user


class LoginSerializer(PersianMessagesMixin, serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            username=attrs["username"],
            password=attrs["password"],
        )
        # One message for both a wrong username and a wrong password, so the
        # form cannot be used to find out which usernames exist.
        if user is None or not user.is_active:
            raise serializers.ValidationError("نام کاربری یا رمز عبور نادرست است.")
        attrs["user"] = user
        return attrs


class ChangePasswordSerializer(PersianMessagesMixin, serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, trim_whitespace=False)
    new_password1 = serializers.CharField(max_length=128, write_only=True, trim_whitespace=False)
    new_password2 = serializers.CharField(max_length=128, write_only=True, trim_whitespace=False)

    def validate_old_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("رمز عبور فعلی نادرست است.")
        return value

    def validate_new_password1(self, value):
        return validate_new_password(value)

    def validate(self, attrs):
        if attrs["new_password1"] != attrs["new_password2"]:
            raise serializers.ValidationError({"new_password2": "رمزهای عبور مطابقت ندارند."})
        return attrs

    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password1"])
        user.save(update_fields=["password"])
        return user


def digits_only(length, message):
    """Builds a validator for fields that must be exactly `length` digits."""
    pattern = re.compile(rf"^\d{{{length}}}$")

    def validate(value):
        if value and not pattern.match(value):
            raise serializers.ValidationError(message)
        return value

    return validate


MOBILE_PATTERN = re.compile(r"^09\d{9}$")


def validate_mobile(value):
    if value and not MOBILE_PATTERN.match(value):
        raise serializers.ValidationError("شماره همراه باید با ۰۹ شروع شود و ۱۱ رقم باشد")
    return value


# Profile fields the old edit form required; the profile counts as complete
# once all of them are filled.
REQUIRED_PROFILE_FIELDS = (
    "national_code",
    "address",
    "zipcode",
    "street",
    "city",
    "mobile",
    "age",
    "card_number",
    "iban",
)

ADDRESS_FIELDS = ("address", "zipcode", "street", "city", "mobile")


class ProfileSerializer(PersianMessagesMixin, serializers.ModelSerializer):
    """Editable profile, together with the account fields of the user."""

    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", max_length=25, required=False)
    last_name = serializers.CharField(source="user.last_name", max_length=25, required=False)
    email = serializers.EmailField(source="user.email", required=False)
    gender = serializers.BooleanField(required=False)
    gender_display = serializers.CharField(source="get_gender_display", read_only=True)
    customer_image = serializers.ImageField(required=False, allow_null=True)
    national_code = serializers.CharField(
        max_length=10, required=False, allow_blank=True,
        validators=[digits_only(10, "کد ملی باید ۱۰ رقم باشد")],
    )
    zipcode = serializers.CharField(
        max_length=20, required=False, allow_blank=True,
        validators=[digits_only(10, "کد پستی باید ۱۰ رقم باشد")],
    )
    mobile = serializers.CharField(
        max_length=11, required=False, allow_blank=True, validators=[validate_mobile]
    )
    card_number = serializers.CharField(
        max_length=16, required=False, allow_blank=True,
        validators=[digits_only(16, "شماره کارت باید ۱۶ رقم باشد")],
    )

    orders_count = serializers.SerializerMethodField()
    completed_orders_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomProfileModel
        fields = [
            "username", "first_name", "last_name", "email",
            "national_code", "address", "zipcode", "street", "city", "mobile",
            "age", "gender", "gender_display", "card_number", "iban", "back_money",
            "customer_image", "is_complete", "orders_count", "completed_orders_count",
        ]
        read_only_fields = ["back_money", "is_complete"]
        extra_kwargs = {
            "address": {"required": False, "allow_blank": True, "allow_null": True},
            "street": {"required": False, "allow_blank": True, "allow_null": True},
            "city": {"required": False, "allow_blank": True, "allow_null": True},
            "iban": {"required": False, "allow_blank": True, "allow_null": True},
            "age": {"required": False, "allow_null": True},
        }

    def get_orders_count(self, profile):
        return Order.objects.filter(customer=profile.user).count()

    def get_completed_orders_count(self, profile):
        return Order.objects.filter(
            customer=profile.user, invoice__transaction__status="completed"
        ).distinct().count()

    def validate_email(self, value):
        taken = CustomUser.objects.filter(email__iexact=value).exclude(pk=self.instance.user_id)
        if taken.exists():
            raise serializers.ValidationError("ایمیل تکراری است")
        return value

    def update(self, profile, validated_data):
        user_data = validated_data.pop("user", {})
        for field, value in user_data.items():
            setattr(profile.user, field, value)
        if user_data:
            profile.user.save()

        for field, value in validated_data.items():
            setattr(profile, field, value)
        profile.is_complete = all(getattr(profile, field) for field in REQUIRED_PROFILE_FIELDS)
        profile.save()
        return profile


class AddressSerializer(PersianMessagesMixin, serializers.ModelSerializer):
    """The delivery address part of the profile."""

    zipcode = serializers.CharField(
        max_length=20, allow_blank=True, validators=[digits_only(10, "کد پستی باید ۱۰ رقم باشد")]
    )
    mobile = serializers.CharField(max_length=11, allow_blank=True, validators=[validate_mobile])

    class Meta:
        model = CustomProfileModel
        fields = list(ADDRESS_FIELDS)
        extra_kwargs = {
            "address": {"allow_blank": True, "allow_null": True},
            "street": {"allow_blank": True, "allow_null": True},
            "city": {"allow_blank": True, "allow_null": True},
        }

    def update(self, profile, validated_data):
        profile = super().update(profile, validated_data)
        profile.is_complete = all(getattr(profile, field) for field in REQUIRED_PROFILE_FIELDS)
        profile.save(update_fields=["is_complete"])
        return profile
