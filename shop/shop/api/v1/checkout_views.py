from decimal import ROUND_HALF_UP, Decimal

from django.core.cache import cache
from django.db import transaction
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.v1.customer_serializers import ADDRESS_FIELDS
from accounts.api.v1.customer_views import get_profile
from cart.cart import Cart
from shop.models import Invoice, Order, OrderItem, Transaction
from shopproject.security import CsrfProtectedMixin

from .public_serializers import OrderSerializer
from .public_views import serialize_cart

# Money columns hold 10 digits with one decimal, so a total must stay below this.
MAX_ORDER_TOTAL = Decimal("999999999")
ONE_DECIMAL = Decimal("0.1")
TWO_DECIMALS = Decimal("0.01")

# A checkout runs for well under this; it only frees the lock if a request dies.
CHECKOUT_LOCK_SECONDS = 30


def acquire_checkout_lock(user_id):
    """Takes the per-customer checkout lock; False when another checkout is running."""
    return cache.add(f"checkout-lock-{user_id}", "1", CHECKOUT_LOCK_SECONDS)


def release_checkout_lock(user_id):
    cache.delete(f"checkout-lock-{user_id}")


def reload_session(session):
    """
    Re-reads the session from its store.

    Authentication loads the session early; a checkout that finished in the
    meantime may already have emptied the cart in the store. Without this the
    waiting request would still see the old cart and place the order again.
    """
    session._session_cache = session.load()


class CheckoutApiView(CsrfProtectedMixin, APIView):
    """
    Turns the session cart into an order of the logged in customer.

    Online payment is not connected yet, so the order is stored with a
    `pending` transaction, exactly as the old checkout page did.
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Checkout"])
    def get(self, request):
        """Cart summary and whether the customer filled in the delivery details."""
        profile = get_profile(request.user)
        address_complete = all(getattr(profile, field) for field in ADDRESS_FIELDS)
        return Response({"cart": serialize_cart(request), "address_complete": address_complete})

    @swagger_auto_schema(tags=["Checkout"])
    def post(self, request):
        # Two clicks or two tabs must not place the same order twice.
        if not acquire_checkout_lock(request.user.pk):
            return Response(
                {"detail": "سفارش شما در حال ثبت است. چند لحظه صبر کنید."},
                status=status.HTTP_409_CONFLICT,
            )
        try:
            return self.place_order(request)
        finally:
            release_checkout_lock(request.user.pk)

    def place_order(self, request):
        reload_session(request.session)
        cart = Cart(request)
        lines = cart.lines()
        if not lines:
            return Response({"detail": "سبد خرید خالی است."}, status=status.HTTP_400_BAD_REQUEST)

        costs = [line["total_price"].quantize(ONE_DECIMAL, ROUND_HALF_UP) for line in lines]
        total = sum(costs, Decimal(0))
        if total > MAX_ORDER_TOTAL:
            return Response(
                {"detail": "مبلغ سفارش بیش از حد مجاز است. تعداد کالاها را کاهش دهید."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            order = Order.objects.create(customer=request.user)
            invoice = Invoice.objects.create(order=order, invoice_date=timezone.now())
            Transaction.objects.create(
                invoice=invoice,
                transaction_date=timezone.now(),
                amount=total,
                status="pending",
            )
            OrderItem.objects.bulk_create(
                OrderItem(
                    order=order,
                    customer=request.user,
                    product=line["product"],
                    product_price=line["price"],
                    discounted_price=line["unit_price"].quantize(TWO_DECIMALS, ROUND_HALF_UP),
                    product_count=line["product_count"],
                    product_cost=cost,
                )
                for line, cost in zip(lines, costs)
            )

        cart.clear()
        order = Order.objects.prefetch_related("orderitem_set__product").get(pk=order.pk)
        return Response(
            OrderSerializer(order, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )
