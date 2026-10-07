from django.conf import settings
from shop.models import Product
from decimal import Decimal


class Cart(object):

    def __init__(self, request):

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

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

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            item = self.cart[str(product.id)]
            item["product"] = product
            item["price"] = Decimal(item["price"])

            if product.offer:
                discount_percent = Decimal(product.offer) / 100
                discount_amount = item["price"] * discount_percent
                item["discounted_price"] = item["price"] - discount_amount
            else:
                item["discounted_price"] = item["price"]

            item["total_price"] = item["discounted_price"] * item["product_count"]
            yield item

    def __len__(self):
        return sum(item["product_count"] for item in self.cart.values())

    def get_total_price(self):
        total_price = sum(
            Decimal(item["discounted_price"]) * item["product_count"]
            for item in self.cart.values()
        )
        return total_price

    def lines(self):
        """
        Read-only view of the cart as plain data.

        Unlike iterating the cart, this does not store model instances in the
        session. Prices come from the current product, so a price change made
        after a product was added is reflected in the cart and in the order.
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
            unit_price = product.price - product.price * Decimal(product.offer or 0) / Decimal(100)
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
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
