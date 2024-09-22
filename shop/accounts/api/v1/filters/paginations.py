import datetime
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class UserFilterResultPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 1000
    now = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M")
            
    def get_paginated_response(self, data):
        
        return Response({
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'total_page' : self.page.paginator.num_pages,
            'time':  self.now,
            'count': self.page.paginator.count,
            'results': data

        })
    

