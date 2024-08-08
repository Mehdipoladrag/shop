from django.views.generic import ListView, DetailView, View
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from cart.forms import CartAddProductForm
from cart.cart import Cart
from decimal import Decimal
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
# Models
from shop.models import (
    Product,
    Category,
    Brand,
    OrderItem,
    Order,
    Transaction,
    Invoice,
)


# Create your views here.
class ShopListView(ListView):
    template_name = "shop/shoplist.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_list"] = Product.objects.all()
        context["categori"] = Category.objects.all()
        context["brands"] = Brand.objects.all()
        return context


class ShopDetailView(DetailView):
    model = Product
    template_name = "shop/shopdetail.html"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        try:
            return Product.objects.get(slug=self.kwargs[self.slug_url_kwarg])
        except Product.DoesNotExist:
            raise Http404("Product does not exist")
        except Product.MultipleObjectsReturned:
            return Product.objects.filter(slug=self.kwargs[self.slug_url_kwarg]).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_add_product_form"] = CartAddProductForm()
        return context


class SearchView(View):
    def get(self, request):
        brands = Brand.objects.all()
        products2 = Product.objects.all()
        q = request.GET.get("q")
        if q:
            products = Product.objects.filter(Q(product_name__icontains=q))
            context = {
                "q": q,
                "products": products,
                "products2": products2,
                "brands": brands,
            }
            return render(request, "shop/search.html", context)
        return render(request, "shop/search.html")


class CategoryListView(ListView):
    model = Product
    template_name = "shop/categoryproductlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(offer__gt=0).order_by(
            "create_date"
        )
        product_list_ids = list(context["products"].values_list("pk", flat=True))
        context["product2"] = Product.objects.filter(product_rate__gt=0).exclude(
            pk__in=product_list_ids
        )
        context["cat"] = Category.objects.all()
        context["brand"] = Brand.objects.all()
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = "shop/detailcat.html"
    context_object_name = "cat"
    slug_url_kwarg = "category_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context["categorlist"] = Category.objects.exclude(pk=category.pk)
        productlist = Product.objects.filter(product_category=category)
        paginator = Paginator(productlist, 9)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["brand"] = Brand.objects.all()
        context["listpage"] = page_obj
        return context

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug is not None:
            queryset = queryset.filter(category_slug=slug)
        obj = get_object_or_404(queryset)
        return obj


class CheckOutView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        if not cart:
            return render(request, "cart/emptycart.html")
        return render(request, "shop/checkout.html", {"cart": cart})

    def post(self, request):
        cart = Cart(request)
        order = None
        order_total_cost = Decimal("0")
        order_items = []
        print("Total Cost:", order_total_cost)
        if request.method == "POST":
            order = Order.objects.create(customer=request.user)
            invoice = Invoice.objects.create(order=order, invoice_date=timezone.now())
            for item in cart:
                product = item["product"]
                product_count = item["product_count"]
                product_price = item["price"]
                discounted_price = item["discounted_price"]

                product_cost = Decimal(product_count) * Decimal(discounted_price)
                item["cost"] = product_cost
                order_total_cost += product_cost

                order_items.append(
                    OrderItem(
                        order=order,
                        customer=request.user,
                        product=product,
                        product_price=product_price,
                        product_count=product_count,
                        product_cost=product_cost,
                    )
                )

            Transaction.objects.create(
                invoice=invoice,
                transaction_date=timezone.now(),
                amount=order_total_cost,
                status="pending",
            )

            OrderItem.objects.bulk_create(
                order_items
            )  # ایجاد همه آیتم‌های سفارش در یک بار

            cart.clear()
            return render(
                request,
                "shop/final_payment.html",
                {"order": order, "total_cost": order_total_cost},
            )

        return render(request, "shop/checkout.html", {"cart": cart})


@login_required
def checkout(request):
    cart = Cart(request)
    if not cart:
        return render(request, "cart/emptycart.html")

    order = None
    order_total_cost = Decimal("0")
    order_items = []  # لیستی برای ذخیره آیتم‌های سفارش

    if request.method == "POST":
        order = Order.objects.create(customer=request.user)
        invoice = Invoice.objects.create(order=order, invoice_date=timezone.now())

        for item in cart:
            product = item["product"]
            product_count = item["product_count"]
            product_price = item["price"]
            discounted_price = item["discounted_price"]

            product_cost = Decimal(product_count) * Decimal(discounted_price)
            item["cost"] = product_cost
            order_total_cost += product_cost

            order_items.append(
                OrderItem(
                    order=order,
                    customer=request.user,
                    product=product,
                    product_price=product_price,
                    product_count=product_count,
                    product_cost=product_cost,
                )
            )

        Transaction.objects.create(
            invoice=invoice,
            transaction_date=timezone.now(),
            amount=order_total_cost,
            status="pending",
        )

        OrderItem.objects.bulk_create(order_items)  # ایجاد همه آیتم‌های سفارش در یک بار

        cart.clear()
        return render(
            request,
            "shop/final_payment.html",
            {"order": order, "total_cost": order_total_cost},
        )

    return render(request, "shop/checkout.html", {"cart": cart})
