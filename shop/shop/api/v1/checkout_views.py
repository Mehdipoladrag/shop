from decimal import ROUND_HALF_UP, Decimal

from django.db import transaction
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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
        return Response({"cart": serialize_cart(request), "profile_complete": profile.is_complete})

    @swagger_auto_schema(tags=["Checkout"])
    def post(self, request):
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
