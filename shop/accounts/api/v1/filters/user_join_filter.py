from rest_framework.filters import BaseFilterBackend, OrderingFilter
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

class UserSearchFilter(BaseFilterBackend):
    search_param = 'search' 
    
    def get_search_terms(self, request):

        params = request.query_params.get(self.search_param, '')
        return params.split()
    
    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        if not search_terms:
            return queryset
        
        query = Q()
        for term in search_terms:

            query |= Q(username__contains=term) | Q(email__contains=term) | Q(first_name__contains=term) | Q(last_name__contains=term)
        
        return queryset.filter(query)
    
class UserProfileSearchFilter(BaseFilterBackend):
    search_param = 'search'
    
    def get_search_terms(self, request):
        params = request.query_params.get(self.search_param, '')
        return params.split()
    
    def validation_mobile(self, mobile):
        if not mobile.startswith('09'):
            raise ValidationError("Mobile number must start with '09'.")
        
    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        if not search_terms:
            return queryset
        
        query = Q()
        for term in search_terms:
            if term.isdigit(): 
                self.validation_mobile(term)
            
            query |= Q(mobile__icontains=term) | Q(gender__icontains=term)
        
        filtered_queryset = queryset.filter(query)
    
        if not filtered_queryset.exists():
            raise ValidationError("No matching records found.")
        
        return filtered_queryset
 
class UserOrderFilter(OrderingFilter):
    VALID_FILTERS = {
        "1day": timedelta(days=1),
        "7days": timedelta(days=7),
        "1month": timedelta(days=30),
        "1year": timedelta(days=365),
    }
    

    def validate_filter(self, date_filter):
        if date_filter and date_filter not in self.VALID_FILTERS:
            raise ValidationError({
                "detail": "Invalid filter parameter. Please use one of the following: 7days, 1month, 1day, 1year."
            }) 

    def filter_queryset(self, request, queryset, view):
        date_filter = request.query_params.get('filter', None)
        today = timezone.now().date()

        self.validate_filter(date_filter)
        if date_filter: 
            start_date = today - self.VALID_FILTERS[date_filter]
            queryset = queryset.filter(date_joined__date__gte=start_date)

        return super().filter_queryset(request, queryset, view)