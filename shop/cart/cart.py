from decimal import Decimal

from django.conf import settings

from shop.models import Product
from shop.pricing import discounted_price


class Cart(object):
    """The shopping cart of a visitor, kept in the session."""

    def __init__(self, request):
        self.session = request.session
        # Reading the cart must not write to the session: that would create and
        # store a new session for every anonymous request.
        self.cart = self.session.get(settings.CART_SESSION_ID) or {}

    def add(self, product, product_count=1, update_count=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"product_count": 0, "price": str(product.price)}

        if update_count:
            self.cart[product_id]["product_count"] = product_count
        else:
            self.cart[product_id]["product_count"] += product_count
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def lines(self):
        """
        Read-only view of the cart as plain data.

        Nothing is stored back in the session, and prices come from the current
        product, so a price change made after a product was added is reflected
        in the cart and in the order.
        """
        products = Product.objects.select_related("product_category", "product_brand").in_bulk(
            [int(product_id) for product_id in self.cart]
        )
        lines = []
        for product_id, entry in self.cart.items():
            product = products.get(int(product_id))
            if product is None:
                continue
            count = entry["product_count"]
            unit_price = discounted_price(product.price, product.offer)
            lines.append(
                {
                    "product": product,
                    "product_count": count,
                    "price": product.price,
                    "unit_price": unit_price,
                    "total_price": unit_price * count,
                }
            )
        return lines

    def clear(self):
        if settings.CART_SESSION_ID in self.session:
            self.session[settings.CART_SESSION_ID] = {}
            self.session.modified = True

    def __len__(self):
        return sum(item["product_count"] for item in self.cart.values())
