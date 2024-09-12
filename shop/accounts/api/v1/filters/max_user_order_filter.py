from rest_framework.filters import OrderingFilter
from django.db.models import Q
from django.db.models import Count


class UserMaxOrderFilter(OrderingFilter):

    def filter_queryset(self, request, queryset, view):

        queryset = queryset.annotate(order_count=Count("customer")).filter(
            order_count__lt=4
        )

        search_terms = request.query_params.get("search", "")
        if not search_terms:
            return queryset

        search_terms = search_terms.split()
        query = Q()
        for term in search_terms:
            query |= (
                Q(customer__username__icontains=term)
                | Q(customer__email__icontains=term)
                | Q(customer__first_name__icontains=term)
                | Q(customer__last_name__icontains=term)
            )

        return queryset.filter(query)
